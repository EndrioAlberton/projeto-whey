import json
from decimal import Decimal
from django.contrib import admin
from django.contrib import messages


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
from django.http import JsonResponse
from django.urls import path
from .models import Marca, Plataforma, Sabor, Tamanho, Produto


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    search_fields = ('nome',)


@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')


@admin.register(Sabor)
class SaborAdmin(admin.ModelAdmin):
    search_fields = ('nome',)


@admin.register(Tamanho)
class TamanhoAdmin(admin.ModelAdmin):
    list_display = ('rotulo', 'peso_g')
    ordering = ('peso_g',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display   = ('marca', 'nome', 'plataforma', 'preco', 'tamanho', 'proteina_g', 'sabor', 'custo_display', 'atualizado_em')
    list_filter    = ('plataforma', 'marca', 'sabor', 'tamanho')
    search_fields  = ('nome', 'marca__nome', 'sabor__nome')
    readonly_fields = ('atualizado_em', 'doses_display', 'custo_por_dose_display', 'custo_30g_display')
    actions        = ['atualizar_precos']
    class Media:
        js = ('admin/js/buscar_link.js',)

    fieldsets = (
        ('Produto', {
            'fields': ('marca', 'nome', 'plataforma', 'sabor', 'url_imagem')
        }),
        ('Dados nutricionais e peso', {
            'fields': ('tamanho', 'dose_g', 'proteina_g', 'doses_display')
        }),
        ('Preço e link', {
            'fields': ('preco', 'url_afiliado', 'custo_por_dose_display', 'custo_30g_display')
        }),
        ('Metadados', {
            'fields': ('atualizado_em',)
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        extra = [
            path('buscar-link/', self.admin_site.admin_view(self.buscar_link_view), name='catalog_produto_buscar_link'),
        ]
        return extra + urls

    def buscar_link_view(self, request):
        if request.method != 'POST':
            return JsonResponse({'erro': 'Método não permitido.'}, status=405)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'erro': 'JSON inválido.'}, status=400)

        url = data.get('url', '').strip()
        if not url:
            return JsonResponse({'erro': 'URL não informada.'}, status=400)

        if 'mercadolivre' in url or 'mercadolibre' in url or 'mlb' in url.lower():
            from .fetchers import fetch_mercadolivre
            dados = fetch_mercadolivre(url)
        elif 'amazon' in url:
            from .fetchers import fetch_amazon
            dados = fetch_amazon(url)
        else:
            return JsonResponse({'erro': 'Plataforma não reconhecida. Use links do Mercado Livre ou Amazon.'}, status=400)

        if 'erro' in dados:
            return JsonResponse(dados, status=400)

        # Matching automático de dropdowns
        peso_g = dados.get('peso_g')
        if peso_g:
            tamanho = Tamanho.objects.filter(peso_g=peso_g).first()
            if tamanho:
                dados['tamanho_id'] = tamanho.id

        brand = dados.get('brand', '')
        if brand:
            marca = _match_nome(brand, Marca.objects.all())
            if marca:
                dados['marca_id'] = marca.id

        nome = dados.get('name', '')
        if nome:
            sabor = _match_nome_em_texto(nome, Sabor.objects.all())
            if sabor:
                dados['sabor_id'] = sabor.id

        plataforma = Plataforma.objects.filter(codigo=dados.get('platform', '')).first()
        if plataforma:
            dados['plataforma_id'] = plataforma.id

        return JsonResponse(dados)

    def atualizar_precos(self, request, queryset):
        from catalog.fetchers import fetch_mercadolivre
        atualizados = erros = 0
        for p in queryset.filter(plataforma__codigo='ML'):
            if not p.url_afiliado or p.url_afiliado == '#':
                continue
            try:
                dados = fetch_mercadolivre(p.url_afiliado)
                if 'erro' in dados or not dados.get('price'):
                    erros += 1
                    continue
                novo = Decimal(str(dados['price']))
                if novo != p.preco:
                    p.preco = novo
                    p.save(update_fields=['preco', 'atualizado_em'])
                atualizados += 1
            except Exception:
                erros += 1
        self.message_user(request, f'{atualizados} preços atualizados, {erros} erros.', messages.SUCCESS if not erros else messages.WARNING)
    atualizar_precos.short_description = 'Atualizar preços via ML'

    def custo_display(self, obj):
        return f'R$ {obj.custo_por_30g_proteina:.2f} / 30g' if obj.custo_por_30g_proteina else '—'
    custo_display.short_description = 'Custo / 30g prot'

    def doses_display(self, obj):
        return f'{obj.doses} doses' if obj.doses else '—'
    doses_display.short_description = 'Doses'

    def custo_por_dose_display(self, obj):
        return f'R$ {obj.custo_por_dose:.2f}' if obj.custo_por_dose else '—'
    custo_por_dose_display.short_description = 'Custo por dose'

    def custo_30g_display(self, obj):
        return f'R$ {obj.custo_por_30g_proteina:.2f}' if obj.custo_por_30g_proteina else '—'
    custo_30g_display.short_description = 'Custo por 30g de proteína'
