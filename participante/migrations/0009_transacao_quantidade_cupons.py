# Generated by Django 3.2.20 on 2024-02-18 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participante', '0008_transacao_payload'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao',
            name='quantidade_cupons',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
