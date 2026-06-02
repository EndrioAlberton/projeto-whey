from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, MarcaViewSet, PlataformaViewSet, SaborViewSet, TamanhoViewSet, buscar_link

router = DefaultRouter()
router.register('produtos',    ProdutoViewSet,    basename='produto')
router.register('marcas',      MarcaViewSet,      basename='marca')
router.register('plataformas', PlataformaViewSet, basename='plataforma')
router.register('sabores',     SaborViewSet,      basename='sabor')
router.register('tamanhos',    TamanhoViewSet,    basename='tamanho')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/buscar-link/', buscar_link),
]
