# Generated by Django 3.2.12 on 2022-05-28 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preguntas_respuestas', '0004_delete_questionsharedhistorial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
