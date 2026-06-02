import django_filters
from .models import Produto


class ProdutoFilter(django_filters.FilterSet):
    marca      = django_filters.CharFilter(field_name='marca__nome',        lookup_expr='iexact')
    sabor      = django_filters.CharFilter(field_name='sabor__nome',        lookup_expr='iexact')
    plataforma = django_filters.CharFilter(field_name='plataforma__codigo', lookup_expr='iexact')
    peso_g     = django_filters.NumberFilter(field_name='tamanho__peso_g')
    proteina_min = django_filters.NumberFilter(field_name='proteina_g',     lookup_expr='gte')

    class Meta:
        model = Produto
        fields = ['marca', 'sabor', 'plataforma', 'peso_g', 'proteina_min']
