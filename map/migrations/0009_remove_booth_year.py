# Generated by Django 4.2.18 on 2025-03-23 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0008_remove_booth_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booth',
            name='year',
        ),
    ]