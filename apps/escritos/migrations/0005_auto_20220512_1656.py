# Generated by Django 3.2.12 on 2022-05-12 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escritos', '0004_delete_termsharedhistorial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termcorrection',
            name='date_approved',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='termcorrection',
            name='term_content_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='escritos.termcontent'),
        ),
    ]
