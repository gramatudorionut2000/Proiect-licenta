# Generated by Django 4.1.5 on 2023-03-31 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DMS', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='document',
            name='short_description',
            field=models.TextField(max_length=100),
        ),
    ]
