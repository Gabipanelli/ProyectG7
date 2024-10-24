# Generated by Django 4.2.3 on 2024-10-22 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('cuerpo', models.TextField()),
                ('imagen', models.ImageField(upload_to='noticias')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('ubicacion', models.CharField(blank=True, max_length=100, null=True)),
                ('categoria_noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noticias.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(max_length=1500)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noticias.noticia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
