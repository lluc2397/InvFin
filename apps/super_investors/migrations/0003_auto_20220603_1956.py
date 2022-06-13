# Generated by Django 3.2.12 on 2022-06-03 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_investors', '0002_auto_20220602_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superinvestor',
            name='fund_name',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='superinvestor',
            name='info_accronym',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='superinvestor',
            name='name',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='superinvestor',
            name='slug',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
    ]
