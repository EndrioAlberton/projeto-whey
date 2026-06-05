import os
import re
import time
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs

_ml_token_cache = {'token': None, 'expires_at': 0}


def _update_env(key: str, value: str):
    env_path = Path(__file__).resolve().parent.parent / '.env'
    content = env_path.read_text(encoding='utf-8') if env_path.exists() else ''
    lines = content.splitlines()
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f'{key}='):
            lines[i] = f'{key}={value}'
            updated = True
            break
    if not updated:
        lines.append(f'{key}={value}')
    env_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _refresh_token() -> str | None:
    refresh_token = os.environ.get('ML_REFRESH_TOKEN')
    app_id = os.environ.get('ML_APP_ID')
    secret = os.environ.get('ML_SECRET')
    if not all([refresh_token, app_id, secret]):
        return None

    resp = requests.post('https://api.mercadolibre.com/oauth/token', data={
        'grant_type':    'refresh_token',
        'client_id':     app_id,
        'client_secret': secret,
        'refresh_token': refresh_token,
    }, timeout=10)

    if resp.status_code != 200:
        return None

    data = resp.json()
    access_token  = data.get('access_token')
    new_refresh   = data.get('refresh_token', refresh_token)

    os.environ['ML_ACCESS_TOKEN']  = access_token
    os.environ['ML_REFRESH_TOKEN'] = new_refresh
    _update_env('ML_ACCESS_TOKEN',  access_token)
    _update_env('ML_REFRESH_TOKEN', new_refresh)

    _ml_token_cache['token']      = access_token
    _ml_token_cache['expires_at'] = time.time() + data.get('expires_in', 21600) - 60
    return access_token


def _get_ml_token() -> str | None:
    global _ml_token_cache

    if _ml_token_cache['token'] and time.time() < _ml_token_cache['expires_at']:
        return _ml_token_cache['token']

    # Tenta renovar via refresh_token primeiro
    token = _refresh_token()
    if token:
        return token

    # Fallback: access_token direto do env (pode estar expirado)
    access_token = os.environ.get('ML_ACCESS_TOKEN')
    if access_token:
        _ml_token_cache['token']      = access_token
        _ml_token_cache['expires_at'] = time.time() + 3600
        return access_token

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
