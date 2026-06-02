from django.core.management.base import BaseCommand
from catalog.models import Produto
from catalog.fetchers import fetch_mercadolivre
from decimal import Decimal


class Command(BaseCommand):
    help = 'Atualiza preços de todos os produtos via API do Mercado Livre'

    def handle(self, *args, **kwargs):
        produtos = Produto.objects.filter(plataforma__codigo='ML')
        total = produtos.count()
        atualizados = 0
        erros = 0

        self.stdout.write(f'Atualizando preços de {total} produtos ML...')

        for p in produtos:
            if not p.url_produto:
                continue

            try:
                dados = fetch_mercadolivre(p.url_produto)

                if 'erro' in dados:
                    self.stdout.write(self.style.WARNING(f'  [{p.id}] {p.nome}: {dados["erro"]}'))
                    erros += 1
                    continue

                novo_preco = dados.get('price')
                if novo_preco and Decimal(str(novo_preco)) != p.preco:
                    preco_antigo = p.preco
                    p.preco = Decimal(str(novo_preco))
                    p.save(update_fields=['preco', 'atualizado_em'])
                    self.stdout.write(f'  [{p.id}] {p.nome}: R$ {preco_antigo} → R$ {p.preco}')
                    atualizados += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [{p.id}] {p.nome}: erro inesperado — {e}'))
                erros += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nConcluído: {atualizados} atualizados, {erros} erros, {total - atualizados - erros} sem alteração.'
        ))
