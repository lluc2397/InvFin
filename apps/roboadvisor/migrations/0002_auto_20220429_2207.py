# Generated by Django 3.2.12 on 2022-04-29 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roboadvisor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investorprofile',
            name='risk_profile',
            field=models.CharField(blank=True, choices=[('very-agressive', 'Perfil muy agresivo'), ('agressive', 'Perfil agresivo'), ('regular', 'Perfil regular'), ('conservative', 'Perfil conservador'), ('very-conservative', 'Perfil muy conservador')], max_length=500),
        ),
        migrations.AlterField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='asset_knowledge',
            field=models.CharField(blank=True, choices=[('expert', 'Experto'), ('pro', 'Profesional'), ('intermediate', 'Intermedio'), ('basic', 'Básico'), ('null', 'Nulo')], default=('null', 'Nulo'), max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='result',
            field=models.CharField(blank=True, choices=[('Comprar', 'buy'), ('Vender', 'sell'), ('Mantener', 'hold'), ('Mantener', 'error')], max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='sector_knowledge',
            field=models.CharField(blank=True, choices=[('expert', 'Experto'), ('pro', 'Profesional'), ('intermediate', 'Intermedio'), ('basic', 'Básico'), ('null', 'Nulo')], default=('null', 'Nulo'), max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='roboadvisorquestioninvestorexperience',
            name='objectif',
            field=models.IntegerField(blank=True, choices=[(1, 'Generar ingresos pasivos'), (2, 'Generar un patrimonio'), (3, 'Ahorrar'), (4, 'Ganar dinero rápido')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='asset_knowledge',
            field=models.CharField(blank=True, choices=[('expert', 'Experto'), ('pro', 'Profesional'), ('intermediate', 'Intermedio'), ('basic', 'Básico'), ('null', 'Nulo')], default=('null', 'Nulo'), max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='sector_knowledge',
            field=models.CharField(blank=True, choices=[('expert', 'Experto'), ('pro', 'Profesional'), ('intermediate', 'Intermedio'), ('basic', 'Básico'), ('null', 'Nulo')], default=('null', 'Nulo'), max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='temporaryinvestorprofile',
            name='risk_profile',
            field=models.CharField(blank=True, choices=[('very-agressive', 'Perfil muy agresivo'), ('agressive', 'Perfil agresivo'), ('regular', 'Perfil regular'), ('conservative', 'Perfil conservador'), ('very-conservative', 'Perfil muy conservador')], max_length=500),
        ),
    ]
