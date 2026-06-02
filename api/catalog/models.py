from django.db import models


class Marca(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nome


class Plataforma(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # ML, AMZ
    nome   = models.CharField(max_length=50)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'

    def __str__(self):
        return self.nome


class Sabor(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Sabor'
        verbose_name_plural = 'Sabores'

    def __str__(self):
        return self.nome


class Tamanho(models.Model):
    peso_g = models.IntegerField(unique=True)
    rotulo = models.CharField(max_length=20)  # Ex: "900g", "1kg", "2kg"

    class Meta:
        ordering = ['peso_g']
        verbose_name = 'Tamanho'
        verbose_name_plural = 'Tamanhos'

    def __str__(self):
        return self.rotulo


class Produto(models.Model):
    marca         = models.ForeignKey(Marca,      on_delete=models.PROTECT, related_name='produtos')
    nome          = models.CharField(max_length=200)
    plataforma    = models.ForeignKey(Plataforma, on_delete=models.PROTECT, related_name='produtos')
    preco         = models.DecimalField(max_digits=8, decimal_places=2)
    tamanho       = models.ForeignKey(Tamanho,    on_delete=models.PROTECT, related_name='produtos')
    dose_g        = models.IntegerField(default=30)
    proteina_g    = models.DecimalField(max_digits=5, decimal_places=1)
    sabor         = models.ForeignKey(Sabor,      on_delete=models.PROTECT, related_name='produtos')
    url_afiliado  = models.URLField()
    url_imagem    = models.URLField(blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['preco']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f'{self.marca} — {self.nome} ({self.plataforma})'

    @property
    def doses(self):
        if not self.tamanho_id or not self.dose_g:
            return None
        return self.tamanho.peso_g // self.dose_g

    @property
    def custo_por_dose(self):
        d = self.doses
        if not d or not self.preco:
            return None
        return round(float(self.preco) / d, 2)

    @property
    def custo_por_30g_proteina(self):
        d = self.doses
        if not d or not self.proteina_g or not self.preco:
            return None
        proteina_total = float(self.proteina_g) * d
        return round((float(self.preco) / proteina_total) * 30, 2)
