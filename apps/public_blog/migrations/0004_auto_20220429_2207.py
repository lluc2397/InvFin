# Generated by Django 3.2.12 on 2022-04-29 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_blog', '0003_auto_20220415_0001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilesharedhistorial',
            name='content_shared',
        ),
        migrations.RemoveField(
            model_name='profilesharedhistorial',
            name='user',
        ),
        migrations.DeleteModel(
            name='BlogSharedHistorial',
        ),
        migrations.DeleteModel(
            name='ProfileSharedHistorial',
        ),
    ]
