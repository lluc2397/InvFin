# Generated by Django 3.2.12 on 2022-04-15 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preguntas_respuestas', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
