from rest_framework import serializers
from .models import Produto, Marca, Plataforma, Sabor, Tamanho


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nome']


class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = ['id', 'codigo', 'nome']


class SaborSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sabor
        fields = ['id', 'nome']


class TamanhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tamanho
        fields = ['id', 'peso_g', 'rotulo']


class ProdutoSerializer(serializers.ModelSerializer):
    marca      = serializers.CharField(source='marca.nome',        read_only=True)
    plataforma = serializers.CharField(source='plataforma.codigo', read_only=True)
    sabor      = serializers.CharField(source='sabor.nome',        read_only=True)
    peso_g     = serializers.IntegerField(source='tamanho.peso_g', read_only=True)

    doses                  = serializers.ReadOnlyField()
    custo_por_dose         = serializers.ReadOnlyField()
    custo_por_30g_proteina = serializers.ReadOnlyField()

    class Meta:
        model = Produto
        fields = [
            'id', 'marca', 'nome', 'plataforma', 'preco',
            'peso_g', 'dose_g', 'proteina_g', 'sabor',
            'url_afiliado', 'url_imagem', 'atualizado_em',
            'doses', 'custo_por_dose', 'custo_por_30g_proteina',
        ]
