from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto, Marca, Plataforma, Sabor, Tamanho
from .serializers import ProdutoSerializer, MarcaSerializer, PlataformaSerializer, SaborSerializer, TamanhoSerializer
from .filters import ProdutoFilter


class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.select_related('marca', 'plataforma', 'sabor', 'tamanho').all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProdutoFilter
    ordering_fields = ['preco', 'proteina_g']
    ordering = ['preco']


class MarcaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer


class PlataformaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plataforma.objects.all()
    serializer_class = PlataformaSerializer


class SaborViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sabor.objects.all()
    serializer_class = SaborSerializer


class TamanhoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tamanho.objects.all()
    serializer_class = TamanhoSerializer


@api_view(['POST'])
@permission_classes([IsAdminUser])
def buscar_link(request):
    url = request.data.get('url', '')
    if not url:
        return Response({'erro': 'URL não informada.'}, status=400)

    if 'mercadolivre' in url or 'mercadolibre' in url or 'mlb' in url.lower():
        from .fetchers import fetch_mercadolivre
        dados = fetch_mercadolivre(url)
    elif 'amazon' in url:
        from .fetchers import fetch_amazon
        dados = fetch_amazon(url)
    else:
        return Response({'erro': 'Plataforma não reconhecida.'}, status=400)

    return Response(dados)
