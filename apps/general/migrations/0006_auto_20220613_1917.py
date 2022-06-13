# Generated by Django 3.2.12 on 2022-06-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0005_currency_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('Nuevo blog', 'Nuevo blog'), ('Nuevo comentario', 'Nuevo comentario'), ('Nuevo voto', 'Nuevo voto'), ('Nuevo seguidor', 'Nuevo seguidor'), ('Nueva pregunta', 'Nueva pregunta'), ('Nueva respuesta', 'Nueva respuesta'), ('Respuesta aceptada', 'Respuesta aceptada'), ('Compra efectuada', 'Compra efectuada'), ('Comenta tu úlitma compra', '¿Qué opinas de tu última compra?')], max_length=500),
        ),
        migrations.DeleteModel(
            name='NotificationsType',
        ),
    ]