# Generated by Django 3.2.12 on 2022-06-12 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('super_investors', '0006_auto_20220611_2057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='period',
            options={'get_latest_by': ['-year', '-period'], 'ordering': ['-year', '-period'], 'verbose_name': 'Period', 'verbose_name_plural': 'Periods'},
        ),
        migrations.AlterModelOptions(
            name='superinvestoractivity',
            options={'get_latest_by': ['period_related'], 'ordering': ['period_related'], 'verbose_name': 'Superinvestor activity', 'verbose_name_plural': 'Superinvestors activity'},
        ),
        migrations.AlterModelOptions(
            name='superinvestorhistory',
            options={'get_latest_by': ['period_related'], 'ordering': ['period_related'], 'verbose_name': 'Superinvestor history', 'verbose_name_plural': 'Superinvestors history'},
        ),
    ]
