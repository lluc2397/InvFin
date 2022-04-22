# Generated by Django 3.2.12 on 2022-04-16 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roboadvisor', '0004_auto_20220416_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roboadvisorservice',
            name='steps',
        ),
        migrations.AddField(
            model_name='roboadvisorservicestep',
            name='service_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='roboadvisor.roboadvisorservice'),
        ),
    ]