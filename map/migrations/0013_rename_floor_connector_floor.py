# Generated by Django 4.2.18 on 2025-03-27 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0012_alter_connector_floor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connector',
            old_name='Floor',
            new_name='floor',
        ),
    ]