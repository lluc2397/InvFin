# Generated by Django 3.2.12 on 2022-04-16 20:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roboadvisor', '0005_auto_20220416_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='capital_invested',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='days_studing',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='number_shares',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='time_studing',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='already_investing',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='amount_time_studied',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='asset_knowledge',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='capital_invested',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='days_studing',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='number_shares',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='period_time_studied',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='sector_knowledge',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='sector_relationship',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestioninvestorexperience',
            name='time_studing',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='days_studing',
        ),
        migrations.RemoveField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='time_studing',
        ),
        migrations.RemoveField(
            model_name='roboadvisorservicestep',
            name='date_finished',
        ),
        migrations.RemoveField(
            model_name='roboadvisorservicestep',
            name='date_started',
        ),
        migrations.RemoveField(
            model_name='roboadvisorservicestep',
            name='status',
        ),
        migrations.AlterField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='capital_invested',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='number_shares',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='roboadvisorservicestep',
            name='service_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='roboadvisor.roboadvisorservice'),
        ),
    ]