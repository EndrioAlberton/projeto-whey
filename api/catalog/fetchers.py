import os
import re
import time
import logging
import requests
from datetime import timedelta
from urllib.parse import urlparse, parse_qs

from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)

# Cache in-process de curta duração: evita bater no banco a cada request.
# A fonte de verdade é a linha MLToken (compartilhada entre todos os workers).
_ml_token_cache = {'token': None, 'expires_at': 0}
_MEM_TTL = 300  # 5 min


def _load_row(lock: bool = False):
    """Retorna a linha única de MLToken (pk=1), criando a partir do .env na
    primeira vez. Com lock=True usa select_for_update (exige transaction)."""
    from catalog.models import MLToken

    MLToken.objects.get_or_create(pk=1, defaults={
        'access_token':  os.environ.get('ML_ACCESS_TOKEN', ''),
        'refresh_token': os.environ.get('ML_REFRESH_TOKEN', ''),
        # sem expires_at => tratado como expirado => renova na primeira chamada
    })
    qs = MLToken.objects.select_for_update() if lock else MLToken.objects
    return qs.get(pk=1)


def _cache_mem(access_token: str):
    _ml_token_cache['token']      = access_token
    _ml_token_cache['expires_at'] = time.time() + _MEM_TTL


def _refresh_token(row) -> str | None:
    """Renova usando o refresh_token da linha e persiste os tokens novos.
    Chamado sob select_for_update, então só um worker renova por vez."""
    app_id = os.environ.get('ML_APP_ID')
    secret = os.environ.get('ML_SECRET')
    if not all([row.refresh_token, app_id, secret]):
        return None

    try:
        resp = requests.post('https://api.mercadolibre.com/oauth/token', data={
            'grant_type':    'refresh_token',
            'client_id':     app_id,
            'client_secret': secret,
            'refresh_token': row.refresh_token,
        }, timeout=10)
    except requests.RequestException as e:
        logger.warning('Falha de rede ao renovar token ML: %s', e)
        return None

    if resp.status_code != 200:
        logger.warning('Erro ao renovar token ML: %s %s', resp.status_code, resp.text[:200])
        return None

    data = resp.json()
    access_token = data.get('access_token')
    row.access_token  = access_token
    row.refresh_token = data.get('refresh_token', row.refresh_token)
    row.expires_at    = timezone.now() + timedelta(seconds=data.get('expires_in', 21600) - 60)
    row.save(update_fields=['access_token', 'refresh_token', 'expires_at', 'atualizado_em'])
    _cache_mem(access_token)
    return access_token


def _get_ml_token() -> str | None:
    # Fast path: cache em memória do próprio processo.
    if _ml_token_cache['token'] and time.time() < _ml_token_cache['expires_at']:
        return _ml_token_cache['token']

    with transaction.atomic():
        row = _load_row(lock=True)

        # Access token ainda válido no banco?
        if row.access_token and row.expires_at and timezone.now() < row.expires_at:
            _cache_mem(row.access_token)
            return row.access_token

        # Expirado (ou sem validade): renova.
        token = _refresh_token(row)
        if token:
            return token

        # Fallback: devolve o access_token atual mesmo possivelmente expirado.
        if row.access_token:
            _cache_mem(row.access_token)
            return row.access_token

    return None


def _extract_ml_ids(url: str) -> dict:
    """Extrai product_id (catálogo) e item_id da URL."""
    parsed = urlparse(url)
    qs     = parse_qs(parsed.query)

    product_id = None
    item_id    = None

    # product_id: /p/MLB18725403
    m = re.search(r'/p/(MLB\d+)', parsed.path, re.IGNORECASE)
    if m:
        product_id = m.group(1).upper()

    # item_id: wid= ou /MLB-XXXXXXX-
    if 'wid' in qs:
        item_id = qs['wid'][0].upper()
    else:
        m2 = re.search(r'/(MLB-\d+)', parsed.path, re.IGNORECASE)
        if m2:
            item_id = m2.group(1).replace('-', '').upper()

    return {'product_id': product_id, 'item_id': item_id}


def fetch_mercadolivre(url: str) -> dict:
    token = _get_ml_token()
    if not token:
        return {'erro': 'Credenciais do Mercado Livre não configuradas.'}

    ids = _extract_ml_ids(url)
    headers = {'Authorization': f'Bearer {token}'}

    # Usa a API de catálogo de produtos (funciona com permissão básica)
    product_id = ids.get('product_id')
    if not product_id:
        return {'erro': 'ID do produto não encontrado na URL. Use um link de catálogo (/p/MLB...).'}

    # Busca dados do produto (nome, imagem, marca, peso)
    r = requests.get(f'https://api.mercadolibre.com/products/{product_id}', headers=headers, timeout=10)
    if r.status_code != 200:
        return {'erro': f'Erro ao buscar produto: {r.status_code}'}

    data = r.json()

    # Extrai atributos
    attrs = {a['id']: a.get('value_name') for a in data.get('attributes', []) if a.get('value_name')}
    peso_raw = attrs.get('NET_WEIGHT') or attrs.get('WEIGHT') or attrs.get('PACKAGE_WEIGHT')
    peso_g = _parse_peso(peso_raw)

    image_url = ''
    pictures = data.get('pictures', [])
    if pictures:
        image_url = pictures[0].get('url', '')

    # Busca menor preço via itens do produto
    preco = None
    r2 = requests.get(f'https://api.mercadolibre.com/products/{product_id}/items?limit=5', headers=headers, timeout=10)
    if r2.status_code == 200:
        results = r2.json().get('results', [])
        precos = [i['price'] for i in results if i.get('price')]
        if precos:
            preco = min(precos)

    return {
        'platform':  'ML',
        'name':      data.get('name', ''),
        'brand':     attrs.get('BRAND', ''),
        'price':     preco,
        'image_url': image_url,
        'peso_g':    peso_g,
    }


def _parse_peso(valor: str | None) -> int | None:
    if not valor:
        return None
    try:
        m = re.search(r'([\d.,]+)\s*(kg|g)', valor, re.IGNORECASE)
        if not m:
            return None
        num = float(m.group(1).replace(',', '.'))
        unidade = m.group(2).lower()
        return int(num * 1000) if unidade == 'kg' else int(num)
    except (ValueError, AttributeError):
        return None


def fetch_amazon(url: str) -> dict:
    return {'erro': 'Integração com Amazon ainda não configurada. Configure as credenciais PA-API.'}
