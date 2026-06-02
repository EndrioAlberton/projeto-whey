from django.core.management.base import BaseCommand
from catalog.models import Marca, Plataforma, Sabor, Tamanho


class Command(BaseCommand):
    help = 'Popula dados iniciais: marcas, sabores, tamanhos e plataformas'

    def handle(self, *args, **kwargs):
        marcas = [
            'Growth Supplements', 'Max Titanium', 'Dux Nutrition', 'Integralmédica',
            'Probiótica', 'Black Skull', 'New Millen', 'Atlhetica Nutrition',
            'Optimum Nutrition', 'Darkness', 'BodyBuilders', 'BRN Foods',
            'Absolut Nutrition', 'Midway', 'True Source',
        ]
        for nome in marcas:
            Marca.objects.get_or_create(nome=nome)

        sabores = [
            'Chocolate', 'Baunilha', 'Morango', 'Cookies and Cream',
            'Natural', 'Coco', 'Caramelo', 'Doce de Leite',
            'Banana', 'Cappuccino', 'Chocolate Branco',
        ]
        for nome in sabores:
            Sabor.objects.get_or_create(nome=nome)

        tamanhos = [
            (900,  '900g'),
            (907,  '907g'),
            (1000, '1kg'),
            (1800, '1,8kg'),
            (2000, '2kg'),
            (2270, '2,27kg'),
            (3000, '3kg'),
        ]
        for peso_g, rotulo in tamanhos:
            Tamanho.objects.get_or_create(peso_g=peso_g, defaults={'rotulo': rotulo})

        plataformas = [
            ('ML',  'Mercado Livre'),
            ('AMZ', 'Amazon'),
        ]
        for codigo, nome in plataformas:
            Plataforma.objects.get_or_create(codigo=codigo, defaults={'nome': nome})

        self.stdout.write(self.style.SUCCESS('Dados iniciais populados com sucesso!'))
