# Generated by Django 3.2.14 on 2022-07-25 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_promotion_promotioncampaign'),
        ('recsys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpromotionrecommended',
            name='model_recommended',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.promotion'),
        ),
        migrations.AlterField(
            model_name='visiteurpromotionrecommended',
            name='model_recommended',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.promotion'),
        ),
    ]
