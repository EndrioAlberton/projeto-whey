import os
import requests
from pathlib import Path
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

APP_ID       = lambda: os.environ.get('ML_APP_ID', '')
SECRET       = lambda: os.environ.get('ML_SECRET', '')
REDIRECT_URI = 'https://whey.endrioalberton.com.br'


@staff_member_required
def ml_autorizar(request):
    # Se veio um code via POST (usuário colou manualmente)
    if request.method == 'POST':
        raw = request.POST.get('code', '').strip()
        if not raw:
            return _page(erro='Cole o código ou a URL antes de confirmar.')
        # Aceita tanto a URL completa quanto só o código
        import re
        match = re.search(r'[?&]code=([^&]+)', raw)
        code = match.group(1) if match else raw
        return _trocar_code(code)

    auth_url = (
        f'https://auth.mercadolivre.com.br/authorization'
        f'?response_type=code'
        f'&client_id={APP_ID()}'
        f'&redirect_uri={REDIRECT_URI}'
        f'&scope=read%20write%20offline_access'
    )

    return _page(auth_url=auth_url)


def _trocar_code(code: str):
    resp = requests.post('https://api.mercadolibre.com/oauth/token', data={
        'grant_type':    'authorization_code',
        'client_id':     APP_ID(),
        'client_secret': SECRET(),
        'code':          code,
        'redirect_uri':  REDIRECT_URI,
    }, timeout=10)

    if resp.status_code != 200:
        return _page(erro=f'Erro ao trocar código: {resp.text}')

    data = resp.json()
    access_token  = data.get('access_token', '')
    refresh_token = data.get('refresh_token', '')

    env_path = Path(__file__).resolve().parent.parent / '.env'
    _update_env(env_path, 'ML_REFRESH_TOKEN', refresh_token)
    _update_env(env_path, 'ML_ACCESS_TOKEN',  access_token)

    os.environ['ML_REFRESH_TOKEN'] = refresh_token
    os.environ['ML_ACCESS_TOKEN']  = access_token

    return HttpResponse('''
    <html><body style="font-family:sans-serif;padding:40px;max-width:600px;margin:0 auto">
      <h2 style="color:#27ae60">✓ Autorizado com sucesso!</h2>
      <p>Token salvo. Agora o botão "Buscar dados" no Admin vai funcionar.</p>
      <a href="/admin/catalog/produto/add/"
         style="display:inline-block;margin-top:12px;padding:10px 20px;background:#417690;
                color:#fff;text-decoration:none;border-radius:4px;font-weight:bold;">
        → Adicionar produto
      </a>
    </body></html>
    ''')


def _page(auth_url=None, erro=None):
    erro_html = f'<p style="color:#c0392b;font-weight:bold">{erro}</p>' if erro else ''
    botao = (
        f'<a href="{auth_url}" target="_blank" '
        f'style="display:inline-block;padding:12px 24px;background:#417690;color:#fff;'
        f'text-decoration:none;border-radius:4px;font-weight:bold;">'
        f'1. Autorizar no Mercado Livre ↗</a>'
    ) if auth_url else ''

    return HttpResponse(f'''
    <html><body style="font-family:sans-serif;padding:40px;max-width:640px;margin:0 auto">
      <h2>Autorizar Mercado Livre</h2>
      {erro_html}
      <p><strong>Passo 1:</strong> Clique no botão abaixo e autorize o app com sua conta ML.</p>
      {botao}
      <p style="margin-top:24px"><strong>Passo 2:</strong>
         Após autorizar, o ML vai redirecionar para uma página que pode dar erro —
         isso é normal. Copie o valor do parâmetro <code>?code=</code> que aparece na URL do navegador.
      </p>
      <p>Exemplo de URL:<br>
         <code style="font-size:12px;color:#555">
           https://whey.endrioalberton.com.br<strong>?code=TG-XXXXXXXX-...</strong>
         </code>
      </p>
      <p><strong>Passo 3:</strong> Cole o código aqui e confirme:</p>
      <form method="post" style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
        <input type="hidden" name="csrfmiddlewaretoken"
               value="$(document.cookie.match(/csrftoken=([^;]+)/)?.[1]||'')">
        <input name="code" type="text" placeholder="Cole aqui a URL completa ou só o código TG-XXXXXXXX-..."
               style="flex:1;min-width:260px;padding:8px 10px;border:1px solid #ccc;border-radius:4px;font-size:13px;">
        <button type="submit"
                style="padding:8px 18px;background:#417690;color:#fff;border:none;border-radius:4px;
                       cursor:pointer;font-size:13px;font-weight:bold;">
          Confirmar
        </button>
      </form>
      <script>
        document.querySelector('[name=csrfmiddlewaretoken]').value =
          document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
      </script>
    </body></html>
    ''')


def _update_env(path: Path, key: str, value: str):
    content = path.read_text(encoding='utf-8') if path.exists() else ''
    lines = content.splitlines()
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f'{key}='):
            lines[i] = f'{key}={value}'
            updated = True
            break
    if not updated:
        lines.append(f'{key}={value}')
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
