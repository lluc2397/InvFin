# Generated by Django 3.2.12 on 2022-05-30 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_auto_20220415_0001'),
        ('cartera', '0007_alter_positionmovement_asset_related'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrimonio',
            name='default_currency',
            field=models.ForeignKey(blank=True, default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.currency'),
        ),
    ]
