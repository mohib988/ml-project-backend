# Generated by Django 5.0.3 on 2024-04-09 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_missinginvoice_location_missinginvoice_pos_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missinginvoice',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
