from django.core.management.base import BaseCommand
from catalog.models import Produto


class Command(BaseCommand):
    help = 'Atualiza preços de todos os produtos via API do Mercado Livre'

    def handle(self, *args, **kwargs):
        produtos = Produto.objects.filter(plataforma__codigo='ML').exclude(url_produto='')
        total = produtos.count()
        ok = erros = 0

        self.stdout.write(f'Atualizando preços de {total} produtos ML...')

        for p in produtos:
            try:
                if p.atualizar_preco() == 'ok':
                    ok += 1
                else:
                    erros += 1
                    estado = 'ocultado (indisponível)' if not p.disponivel else 'falha'
                    self.stdout.write(self.style.WARNING(f'  [{p.id}] {p.nome}: {estado}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [{p.id}] {p.nome}: erro inesperado — {e}'))
                erros += 1

        self.stdout.write(self.style.SUCCESS(f'\nConcluído: {ok} atualizados, {erros} com erro/indisponíveis.'))
