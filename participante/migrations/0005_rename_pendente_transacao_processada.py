# Generated by Django 3.2.20 on 2024-02-18 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participante', '0004_auto_20240218_0114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transacao',
            old_name='pendente',
            new_name='processada',
        ),
    ]
