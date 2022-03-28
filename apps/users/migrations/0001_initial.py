# Generated by Django 3.2.12 on 2022-03-28 15:59

import apps.general.mixins
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, max_length=2550, verbose_name='Nombre')),
                ('last_name', models.CharField(blank=True, max_length=2550, verbose_name='Apellidos')),
                ('is_writter', models.BooleanField(default=False)),
                ('just_newsletter', models.BooleanField(default=False)),
                ('just_correction', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='MetaProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=10000, null=True)),
                ('country_code', models.CharField(blank=True, max_length=10000, null=True)),
                ('country_name', models.CharField(blank=True, max_length=10000, null=True)),
                ('dma_code', models.CharField(blank=True, max_length=10000, null=True)),
                ('is_in_european_union', models.BooleanField(default=False)),
                ('latitude', models.CharField(blank=True, max_length=10000, null=True)),
                ('longitude', models.CharField(blank=True, max_length=10000, null=True)),
                ('city', models.CharField(blank=True, max_length=10000, null=True)),
                ('region', models.CharField(blank=True, max_length=10000, null=True)),
                ('time_zone', models.CharField(blank=True, max_length=10000, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10000, null=True)),
                ('continent_code', models.CharField(blank=True, max_length=10000, null=True)),
                ('continent_name', models.CharField(blank=True, max_length=10000, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=10000, null=True)),
            ],
            options={
                'verbose_name': 'Meta profile info',
                'db_table': 'meta_profile_info',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reputation_score', models.IntegerField(default=0)),
                ('creditos', models.IntegerField(default=0)),
                ('edad', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento (DD/MM/AAAA)')),
                ('pais', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='País de origen')),
                ('ciudad', models.CharField(blank=True, max_length=150, null=True, verbose_name='Ciudad de origen')),
                ('foto_perfil', models.ImageField(default='inversorinteligente.WebP', upload_to='avatar/', verbose_name='Foto de perfil')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('ref_code', models.CharField(blank=True, max_length=1000, unique=True)),
                ('recommended_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Users profile',
                'db_table': 'profiles',
            },
            bases=(models.Model, apps.general.mixins.ResizeImageMixin),
        ),
        migrations.CreateModel(
            name='MetaProfileHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.metaprofile')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meta_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Meta profile historial',
                'db_table': 'meta_profile_historial',
            },
        ),
    ]
