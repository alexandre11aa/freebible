# Generated by Django 5.1.1 on 2024-09-19 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bible', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='testamento',
            field=models.CharField(choices=[('N', 'Novo'), ('V', 'Velho')], max_length=1, verbose_name='Testamento'),
        ),
        migrations.AlterField(
            model_name='versiculo',
            name='numero',
            field=models.PositiveIntegerField(verbose_name='Número do Versículo'),
        ),
    ]
