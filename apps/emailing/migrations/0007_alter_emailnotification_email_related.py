# Generated by Django 3.2.12 on 2022-03-16 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
        ('emailing', '0006_auto_20220313_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailnotification',
            name='email_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='email_related', to='general.notification'),
        ),
    ]