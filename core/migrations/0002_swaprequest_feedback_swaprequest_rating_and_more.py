# Generated by Django 5.2.1 on 2025-07-12 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='swaprequest',
            name='feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='swaprequest',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='swap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='core.swaprequest'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='swap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_entries', to='core.swaprequest'),
        ),
    ]
