# Generated by Django 3.2.20 on 2024-02-18 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participante', '0007_auto_20240218_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao',
            name='payload',
            field=models.TextField(blank=True, null=True),
        ),
    ]