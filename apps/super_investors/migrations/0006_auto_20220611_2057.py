# Generated by Django 3.2.12 on 2022-06-11 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0007_institutionalorganization_topinstitutionalownership'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('super_investors', '0005_auto_20220604_0107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='period',
            options={'get_latest_by': ['period', 'year'], 'ordering': ['period', 'year'], 'verbose_name': 'Period', 'verbose_name_plural': 'Periods'},
        ),
        migrations.RemoveField(
            model_name='superinvestoractivity',
            name='reported_price',
        ),
        migrations.RemoveField(
            model_name='superinvestoractivity',
            name='shares',
        ),
        migrations.CreateModel(
            name='SuperinvestorHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.TextField(blank=True, null=True)),
                ('not_registered_company', models.BooleanField(default=False)),
                ('need_verify_company', models.BooleanField(default=False)),
                ('portfolio_change', models.FloatField(blank=True, null=True)),
                ('movement', models.CharField(blank=True, max_length=500, null=True)),
                ('shares', models.FloatField(blank=True, null=True)),
                ('reported_price', models.FloatField(blank=True, null=True)),
                ('portfolio_weight', models.FloatField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresas.company')),
                ('period_related', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='super_investors.period')),
                ('superinvestor_related', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='history', to='super_investors.superinvestor')),
            ],
            options={
                'verbose_name': 'Superinvestor history',
                'verbose_name_plural': 'Superinvestors history',
                'db_table': 'superinvestors_history',
            },
        ),
        migrations.CreateModel(
            name='FavoritesSuperinvestorsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('superinvestor', models.ManyToManyField(blank=True, to='super_investors.Superinvestor')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favorites_superinvestors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Lista de superinvestor favoritas',
                'verbose_name_plural': 'Lista de superinvestor favoritas',
                'db_table': 'favorites_superinvestor_list',
            },
        ),
        migrations.CreateModel(
            name='FavoritesSuperinvestorsHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('added', models.BooleanField(default=False)),
                ('removed', models.BooleanField(default=False)),
                ('superinvestor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='super_investors.superinvestor')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Superinvestor favorita',
                'verbose_name_plural': 'Superinvestor favoritas',
                'db_table': 'favorites_superinvestor_historial',
            },
        ),
    ]
