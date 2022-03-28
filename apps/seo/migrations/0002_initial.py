# Generated by Django 3.2.12 on 2022-03-28 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersjourney',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='metaparametershistorial',
            name='parameter_settings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seo.metaparameters'),
        ),
        migrations.AddField(
            model_name='metaparameters',
            name='meta_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
