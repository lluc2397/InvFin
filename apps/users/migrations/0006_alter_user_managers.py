# Generated by Django 3.2.14 on 2022-07-25 20:52

import apps.users.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_creditusagehistorial_move_source'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', apps.users.managers.UserExtraManager()),
            ],
        ),
    ]
