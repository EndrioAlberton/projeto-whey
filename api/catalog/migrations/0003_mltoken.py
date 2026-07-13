# Token ML compartilhado entre workers.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_add_url_produto'),
    ]

    operations = [
        migrations.CreateModel(
            name='MLToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(blank=True)),
                ('refresh_token', models.TextField(blank=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Token Mercado Livre',
                'verbose_name_plural': 'Token Mercado Livre',
            },
        ),
    ]
