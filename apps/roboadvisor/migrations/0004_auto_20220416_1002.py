# Generated by Django 3.2.12 on 2022-04-16 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roboadvisor', '0003_auto_20220416_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='roboadvisorservicestep',
            name='template',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='roboadvisorservicestep',
            name='url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]