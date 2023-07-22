# Generated by Django 4.1.5 on 2023-03-27 09:11

import DMS.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=100)),
                ('short_description', models.TextField(max_length=20)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.TextField(max_length=255)),
                ('extension', models.CharField(max_length=5)),
                ('document', models.FileField(upload_to=DMS.models.Document.get_upload_path)),
                ('is_global', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
            ],
        ),
    ]