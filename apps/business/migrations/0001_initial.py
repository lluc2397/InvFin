# Generated by Django 3.2.12 on 2022-06-05 23:11

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('general', '0004_auto_20220604_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('stripe_id', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'db_table': 'business_customers',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(blank=True, max_length=300, null=True)),
                ('stripe_id', models.CharField(blank=True, max_length=500, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('image', models.CharField(blank=True, max_length=500, null=True)),
                ('video', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('visits', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'business_products',
            },
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('content_related', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_related', to='business.product')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products comments',
                'db_table': 'business_products_comments',
            },
        ),
        migrations.CreateModel(
            name='ProductComplementary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(blank=True, max_length=300, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('payment_type', models.CharField(blank=True, choices=[('subscription', 'Subscripción'), ('payment', 'Un pago')], max_length=300)),
                ('stripe_id', models.CharField(blank=True, max_length=500, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('subscription_period', models.CharField(blank=True, choices=[('day', 'Daily'), ('week', 'Weekly'), ('month', 'Montly'), ('year', 'Yearly')], max_length=300)),
                ('subscription_interval', models.IntegerField(blank=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('extras', models.JSONField(default=dict)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.currency')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complementary', to='business.product')),
            ],
            options={
                'verbose_name': 'Product complementary',
                'verbose_name_plural': 'Products complementary',
                'db_table': 'business_products_complementary',
            },
        ),
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('discount', models.FloatField(blank=True, null=True)),
                ('is_percentage', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.product')),
                ('product_complementary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.productcomplementary')),
            ],
            options={
                'verbose_name': 'Product discount',
                'verbose_name_plural': 'Products discounts',
                'db_table': 'business_products_discounts',
            },
        ),
        migrations.CreateModel(
            name='TransactionHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(blank=True, choices=[('credits', 'Credits'), ('wire', 'Wire'), ('paypal', 'Paypal'), ('other', 'Others'), ('card', 'Card')], max_length=300)),
                ('final_amount', models.FloatField(blank=True, null=True)),
                ('stripe_response', models.JSONField(blank=True, default=dict, null=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.currency')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.customer')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.productdiscount')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.product')),
                ('product_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.productcomment')),
                ('product_complementary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.productcomplementary')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'db_table': 'business_transactions',
            },
        ),
        migrations.CreateModel(
            name='ProductSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='business.product')),
                ('product_complementary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complementary_subs', to='business.productcomplementary')),
                ('subscriber', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product subscriber',
                'verbose_name_plural': 'Products subscribers',
                'db_table': 'business_products_subscribers',
            },
        ),
        migrations.CreateModel(
            name='ProductComplementaryPaymentLunk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
                ('stripe_id', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('product_complementary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_links', to='business.productcomplementary')),
            ],
            options={
                'verbose_name': 'Product complementary payment link',
                'verbose_name_plural': 'Products complementary payment link',
                'db_table': 'business_products_complementary_payment_link',
            },
        ),
    ]
