# Generated by Django 4.2.18 on 2025-03-27 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0011_remove_floor_connector_connector_floor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connector',
            name='Floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='connectors', to='map.floor'),
        ),
    ]