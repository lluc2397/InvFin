# Generated by Django 3.2.12 on 2022-06-04 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_auto_20220415_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='iso',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='currency', to='general.country'),
        ),
        migrations.AddField(
            model_name='currency',
            name='decimals',
            field=models.IntegerField(blank=True, default=2),
        ),
        migrations.AddField(
            model_name='currency',
            name='iso',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
