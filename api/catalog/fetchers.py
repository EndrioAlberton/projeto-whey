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


def _fetch_product_details(product_id: str, token: str) -> dict:
    """Busca nome/marca/preço/imagem/peso de um product_id de catálogo já
    conhecido. Usada tanto pelo fetch de 1 link (fetch_mercadolivre) quanto
    pela importação em massa (buscar_produtos_ml)."""
    headers = {'Authorization': f'Bearer {token}'}

    r = requests.get(f'https://api.mercadolibre.com/products/{product_id}', headers=headers, timeout=10)
    if r.status_code != 200:
        # 404/410 = produto removido do catálogo; outros códigos podem ser falha transitória
        return {'erro': f'Erro ao buscar produto {product_id}: {r.status_code}',
                'indisponivel': r.status_code in (404, 410)}

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
    sem_ofertas = False
    r2 = requests.get(f'https://api.mercadolibre.com/products/{product_id}/items?limit=5', headers=headers, timeout=10)
    if r2.status_code == 200:
        results = r2.json().get('results', [])
        precos = [i['price'] for i in results if i.get('price')]
        if precos:
            preco = min(precos)
        else:
            sem_ofertas = True  # produto existe mas ninguém vende mais

    # "O que você precisa saber" pode vir em short_description ou em main_features (lista de bullets)
    descricao = '\n'.join(
        [(data.get('short_description') or {}).get('content', '')]
        + [f.get('text', '') for f in data.get('main_features') or []]
    )
    dose = (_extrair_dose_atributos(data.get('attributes', []))
            or _extrair_dose(descricao) or _extrair_dose(data.get('name', ''))
            or _extrair_dose_combinada(data.get('attributes', []), descricao))

    return {
        'proteina_g': dose[0] if dose else None,
        'dose_g':     dose[1] if dose else None,
        'indisponivel': sem_ofertas or data.get('status') == 'inactive',
        'platform':   'ML',
        'product_id': product_id,
        'name':       data.get('name', ''),
        'brand':      attrs.get('BRAND', ''),
        'price':      preco,
        'image_url':  image_url,
        'peso_g':     peso_g,
    }


def fetch_mercadolivre(url: str) -> dict:
    token = _get_ml_token()
    if not token:
        return {'erro': 'Credenciais do Mercado Livre não configuradas.'}

    product_id = _extract_ml_ids(url).get('product_id')
    if not product_id:
        return {'erro': 'ID do produto não encontrado na URL. Use um link de catálogo (/p/MLB...).'}

    return _fetch_product_details(product_id, token)


# Endpoints candidatos pra busca por termo. O ML restringe acesso a cada um
# dependendo do app/permissão liberada, então tentamos em ordem e detectamos
# em runtime qual responde 200 — sem precisar validar isso manualmente antes.
_SEARCH_ENDPOINTS = [
    ('catalog', 'https://api.mercadolibre.com/products/search',
     lambda termo, limit, offset: {'status': 'active', 'site_id': 'MLB', 'q': termo, 'limit': limit, 'offset': offset}),
    ('site', 'https://api.mercadolibre.com/sites/MLB/search',
     lambda termo, limit, offset: {'q': termo, 'limit': limit, 'offset': offset}),
]


def search_mercadolivre(termo: str, limit: int = 50, offset: int = 0, token: str | None = None,
                         endpoint: str | None = None) -> dict:
    """Busca produtos por termo no ML. Tenta a API de catálogo
    (/products/search) e, se não responder 200, cai pra busca geral do site
    (/sites/MLB/search). Passe `endpoint` ('catalog' ou 'site') pra pular a
    tentativa e ir direto num deles (usado por buscar_produtos_ml pra não
    retestar os dois a cada página). Retorna o JSON bruto da resposta (com
    uma chave extra '_endpoint' indicando qual funcionou) ou {'erro': ...}."""
    token = token or _get_ml_token()
    if not token:
        return {'erro': 'Credenciais do Mercado Livre não configuradas.'}

    headers = {'Authorization': f'Bearer {token}'}
    limit = min(limit, 50)

    candidatos = [e for e in _SEARCH_ENDPOINTS if endpoint is None or e[0] == endpoint]
    ultimo_erro = None
    for nome, url, montar_params in candidatos:
        params = montar_params(termo, limit, offset)
        try:
            r = requests.get(url, headers=headers, params=params, timeout=15)
        except requests.RequestException as e:
            ultimo_erro = f'Erro de rede na busca ({nome}): {e}'
            continue
        if r.status_code == 200:
            data = r.json()
            data['_endpoint'] = nome
            return data
        ultimo_erro = f'Erro na busca "{termo}" ({nome}): {r.status_code} {r.text[:200]}'

    return {'erro': ultimo_erro or 'Nenhum endpoint de busca disponível.'}


def buscar_produtos_ml(termo: str, max_resultados: int = 30, sleep: float = 0.4):
    """Generator: busca `termo` no ML, pagina, deduplica por product_id e
    resolve os detalhes de cada produto encontrado (reaproveitando
    _fetch_product_details). Yield um dict por produto no mesmo formato de
    fetch_mercadolivre (com 'product_id') ou {'erro': ...} se a busca falhar."""
    vistos = set()
    coletados = 0
    offset = 0
    endpoint_escolhido = None
    PAGE = 50

    while coletados < max_resultados:
        token = _get_ml_token()
        if not token:
            yield {'erro': 'Credenciais do Mercado Livre não configuradas.'}
            return

        pagina = search_mercadolivre(
            termo, limit=min(PAGE, max_resultados - coletados), offset=offset,
            token=token, endpoint=endpoint_escolhido,
        )
        if 'erro' in pagina:
            yield pagina
            return
        endpoint_escolhido = pagina.get('_endpoint', endpoint_escolhido)

        results = pagina.get('results', [])
        if not results:
            break

        for item in results:
            pid = item.get('catalog_product_id') or item.get('id')
            if not pid or pid in vistos:
                continue
            vistos.add(pid)

            time.sleep(sleep)  # evita estourar rate limit do ML
            detalhe = _fetch_product_details(pid, token)
            if 'erro' in detalhe:
                # fallback: usa os dados crus do próprio resultado de busca
                item_attrs = {a.get('id'): a.get('value_name')
                              for a in item.get('attributes', []) if a.get('value_name')}
                detalhe = {
                    'platform':   'ML',
                    'product_id': pid,
                    'name':       item.get('title') or item.get('name', ''),
                    'brand':      item_attrs.get('BRAND', ''),
                    'price':      item.get('price'),
                    'image_url':  item.get('thumbnail', ''),
                    'peso_g':     _parse_peso(item_attrs.get('NET_WEIGHT') or item_attrs.get('WEIGHT')
                                               or item_attrs.get('PACKAGE_WEIGHT')),
                }

            coletados += 1
            yield detalhe
            if coletados >= max_resultados:
                break

        offset += len(results)
        total = pagina.get('paging', {}).get('total', offset)
        if offset >= total:
            break


def _extrair_dose(texto: str) -> tuple[float, int] | None:
    """Acha "21g de proteína por dose de 30g" (ou "porção") na descrição.
    Retorna (proteina_g, dose_g) ou None. Exige os dois números juntos pra
    não confundir com "proteína total do pote" ou outros gramas soltos."""
    if not texto:
        return None
    prot_re = r'(\d{1,2}(?:[.,]\d)?)\s*g\s*(?:de\s+)?prote[ií]nas?'
    dose_re = r'(?:dose|por[cç][aã]o|scoop|medida)s?\s*(?:de\s+|\(\s*)?(\d{2,3})\s*g'
    # "21g de proteína por dose de 30g"
    m = re.search(prot_re + r'\s+(?:por|em cada|na)\s+' + dose_re, texto, re.IGNORECASE)
    if m:
        prot, dose = m.group(1), m.group(2)
    else:
        # "cada porção de 30g fornece 17g de proteínas"
        m = re.search(dose_re + r'[^.]{0,40}?' + prot_re, texto, re.IGNORECASE)
        if not m:
            return None
        dose, prot = m.group(1), m.group(2)
    prot, dose = float(prot.replace(',', '.')), int(dose)
    return (prot, dose) if 5 <= prot <= 40 and 10 <= dose <= 100 and prot < dose else None


def _extrair_dose_atributos(atributos: list) -> tuple[float, int] | None:
    """Ficha técnica do ML: "Peso da porção: 50 g" + texto livre em "Valores
    nutricionais por porção" com "proteínas 17g". Casa pelo NOME do atributo
    (o ID varia por categoria). Retorna (proteina_g, dose_g) ou None."""
    por_nome = {(a.get('name') or '').lower(): a.get('value_name') or '' for a in atributos}
    dose = _parse_peso(next((v for k, v in por_nome.items() if 'peso da por' in k), None))
    texto = next((v for k, v in por_nome.items() if 'valores nutricionais' in k), '')
    # "27 g proteínas" ou "proteínas 17g" / "proteína: 17g"
    m = re.search(r'(\d{1,2}(?:[.,]\d)?)\s*g\s*(?:de\s+)?prote[ií]nas?|prote[ií]nas?\s*:?\s*(\d{1,2}(?:[.,]\d)?)\s*g\b',
                  texto, re.IGNORECASE)
    if not (dose and m):
        return None
    prot = float((m.group(1) or m.group(2)).replace(',', '.'))
    return (prot, dose) if 5 <= prot <= 40 and 10 <= dose <= 100 and prot < dose else None


def _extrair_dose_combinada(atributos: list, texto: str) -> tuple[float, int] | None:
    """Proteína dita "por porção/dose" num texto SEM o número da dose
    ("21g de proteína pura por porção...") + dose da ficha técnica ("Peso da
    porção: 30 g"). Exige o "por porção/dose" pra não pegar proteína de pote
    ("21g de proteína do soro") e a dose dentro de 10–100g (vendedores às
    vezes põem o peso do pote ali)."""
    dose = _parse_peso(next((a.get('value_name') for a in atributos
                             if 'peso da por' in (a.get('name') or '').lower()), None))
    m = re.search(r'(\d{1,2}(?:[.,]\d)?)\s*g\s*(?:de\s+)?prote[ií]nas?(?:\s+\w+)?\s+por\s+(?:dose|por[cç][aã]o)',
                  texto or '', re.IGNORECASE)
    if not (dose and m):
        return None
    prot = float(m.group(1).replace(',', '.'))
    return (prot, dose) if 5 <= prot <= 40 and 10 <= dose <= 100 and prot < dose else None


def _extrair_proteina_titulo(nome: str) -> int | None:
    """Tentativa best-effort de achar a proteína por dose no título do
    anúncio (ex.: "... 24g de proteína por dose ..."). NÃO confiável — serve
    só de sugestão impressa no console pra acelerar o preenchimento manual.
    proteina_g nunca é gravado a partir daqui."""
    if not nome:
        return None
    m = re.search(
        r'(\d{1,2})\s*g\.?\s*(?:de\s+)?prote[ií]na|prote[ií]na\D{0,10}?(\d{1,2})\s*g\b',
        nome, re.IGNORECASE,
    )
    if not m:
        return None
    valor = int(m.group(1) or m.group(2))
    return valor if 5 <= valor <= 40 else None


def _match_nome(busca: str, queryset) -> object | None:
    """Compara o texto buscado com os objetos do queryset de forma flexível."""
    busca_l = busca.lower()
    busca_palavras = set(busca_l.split())
    for obj in queryset:
        obj_l = obj.nome.lower()
        obj_palavras = set(obj_l.split())
        # Match exato, substring ou ao menos uma palavra em comum
        if obj_l in busca_l or busca_l in obj_l or busca_palavras & obj_palavras:
            return obj
    return None


def _match_nome_em_texto(texto: str, queryset) -> object | None:
    """Procura o nome de cada objeto dentro do texto do produto."""
    texto_l = texto.lower()
    for obj in queryset:
        if obj.nome.lower() in texto_l:
            return obj
    return None


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
