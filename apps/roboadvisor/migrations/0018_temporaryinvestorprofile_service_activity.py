# Generated by Django 3.2.12 on 2022-04-27 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roboadvisor', '0017_auto_20220427_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaryinvestorprofile',
            name='service_activity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserserviceactivity'),
        ),
    ]
