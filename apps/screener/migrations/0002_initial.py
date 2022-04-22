# Generated by Django 3.2.12 on 2022-03-28 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('screener', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('empresas', '0002_initial'),
        ('etfs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userscreenersimpleprediction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userscreenermediumprediction',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresas.company'),
        ),
        migrations.AddField(
            model_name='userscreenermediumprediction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usercompanyobservation',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_foda', to='empresas.company'),
        ),
        migrations.AddField(
            model_name='usercompanyobservation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favoritesstockslist',
            name='stock',
            field=models.ManyToManyField(blank=True, to='empresas.Company'),
        ),
        migrations.AddField(
            model_name='favoritesstockslist',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favorites_companies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favoritesstockshistorial',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresas.company'),
        ),
        migrations.AddField(
            model_name='favoritesstockshistorial',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favoritesetfslist',
            name='etf',
            field=models.ManyToManyField(blank=True, to='etfs.Etf'),
        ),
        migrations.AddField(
            model_name='favoritesetfslist',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favoritesetfshistorial',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='etfs.etf'),
        ),
        migrations.AddField(
            model_name='favoritesetfshistorial',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]