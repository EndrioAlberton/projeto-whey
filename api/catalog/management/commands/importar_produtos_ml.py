from django.core.management.base import BaseCommand
from catalog.models import Marca, Plataforma, Produto, Sabor, Tamanho
from catalog.fetchers import buscar_produtos_ml, _match_nome_em_texto, _extrair_proteina_titulo


def _rotulo(peso_g: int) -> str:
    if peso_g % 1000 == 0:
        return f'{peso_g // 1000}kg'
    if peso_g > 1000:
        return f'{peso_g / 1000:.2f}'.rstrip('0').rstrip('.').replace('.', ',') + 'kg'
    return f'{peso_g}g'


class Command(BaseCommand):
    help = 'Importa produtos do Mercado Livre em massa via busca por termo'

    def add_arguments(self, parser):
        parser.add_argument('termo', type=str, help='Termo de busca, ex: "whey protein"')
        parser.add_argument('--limit', type=int, default=30, help='Máximo de produtos a importar (padrão 30)')
        parser.add_argument('--sleep', type=float, default=0.4, help='Delay em segundos entre chamadas à API (padrão 0.4)')
        parser.add_argument('--dry-run', action='store_true', help='Só mostra o que seria importado, não grava nada')

    def handle(self, *args, **opts):
        termo = opts['termo']
        limit = opts['limit']
        dry = opts['dry_run']

        try:
            plataforma = Plataforma.objects.get(codigo='ML')
        except Plataforma.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Plataforma ML não cadastrada. Rode "python manage.py popular_dados" primeiro.'
            ))
            return

        criados = existentes = ignorados = 0
        self.stdout.write(f'Buscando "{termo}" no Mercado Livre (limite {limit})...\n')

        for c in buscar_produtos_ml(termo, max_resultados=limit, sleep=opts['sleep']):
            if 'erro' in c:
                self.stdout.write(self.style.ERROR(f'  {c["erro"]}'))
                ignorados += 1
                continue

            pid = c['product_id']
            nome = c.get('name') or '(sem nome)'

            if Produto.objects.filter(url_produto__icontains=pid).exists():
                self.stdout.write(f'  [já existe] {nome[:60]}')
                existentes += 1
                continue

            if not c.get('brand') or not c.get('peso_g') or not c.get('price'):
                self.stdout.write(self.style.WARNING(
                    f'  [incompleto — ignorado] {nome[:60]} '
                    f'(marca={c.get("brand") or "?"} peso={c.get("peso_g") or "?"} preco={c.get("price") or "?"})'
                ))
                ignorados += 1
                continue

            # só marcas já cadastradas (lista curada no Admin); match exato, o flexível pega "Nutrition" de qualquer uma
            marca = Marca.objects.filter(nome__iexact=c['brand'].strip()).first()
            if not marca:
                self.stdout.write(self.style.WARNING(f'  [marca fora da lista — ignorado] {nome[:60]} (marca={c["brand"]})'))
                ignorados += 1
                continue
            tamanho, _ = Tamanho.objects.get_or_create(
                peso_g=c['peso_g'], defaults={'rotulo': _rotulo(c['peso_g'])}
            )
            sabor = _match_nome_em_texto(nome, Sabor.objects.all())
            if not sabor:
                sabor, _ = Sabor.objects.get_or_create(nome='Não especificado')

            proteina_sugerida = _extrair_proteina_titulo(nome)

            self.stdout.write(
                f'  [{"seria criado" if dry else "criado"}] {nome[:60]} | '
                f'marca={marca.nome} tamanho={tamanho.rotulo} sabor={sabor.nome} '
                f'preco=R${c["price"]} proteina_sugerida={proteina_sugerida or "?"}g (REVISAR NO ADMIN)'
            )

            if not dry:
                Produto.objects.create(
                    marca=marca,
                    nome=nome[:200],
                    plataforma=plataforma,
                    preco=c['price'],
                    tamanho=tamanho,
                    proteina_g=c.get('proteina_g') or 0,
                    dose_g=c.get('dose_g') or 30,
                    sabor=sabor,
                    url_produto=f'https://www.mercadolivre.com.br/p/{pid}',
                    url_imagem=c.get('image_url', ''),
                )
            criados += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n{criados} {"seriam criados" if dry else "criados"}, '
            f'{existentes} já existiam, {ignorados} ignorados.'
        ))
        if not dry and criados:
            self.stdout.write(self.style.WARNING(
                f'{criados} produtos ficam ocultos em /api/produtos/ até preencher "proteina_g" no Admin '
                f'(filtro "revisão de proteína" na listagem de Produto) — e sem link de afiliado até configurar manualmente.'
            ))
