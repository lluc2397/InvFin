# Generated by Django 3.2.12 on 2022-06-20 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0003_alter_metaprofile_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditUsageHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveBigIntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('initial', models.IntegerField()),
                ('final', models.IntegerField()),
                ('movement', models.IntegerField(choices=[(1, 'Added'), (2, 'Used')])),
                ('move_source', models.CharField(choices=[('excel_usage', 'EXCEL USAGE'), ('excel_gift', 'EXCEL GIFT'), ('bought_credits', 'BOUGHT Credits'), ('screener_usage', 'SCREENER USAGE'), ('prize', 'PRIZE'), ('api_usage', 'API USAGE'), ('question_upvote', 'QUESTION UPVOTE'), ('answer_upvote', 'ANSWER UPVOTE'), ('answer_approved', 'ANSWER APPROVED'), ('term_correction', 'TERM CORRECTION'), ('bought_product', 'BOUGHT Product'), ('roboadvisor_usage', 'Roboadvisor Usage')], max_length=100)),
                ('has_enought_credits', models.BooleanField(default=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credits_historial', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Users credits historial',
                'db_table': 'user_credits_historial',
            },
        ),
    ]
