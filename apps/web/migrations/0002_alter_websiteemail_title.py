# Generated by Django 3.2.12 on 2022-04-15 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websiteemail',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]
