# Generated by Django 4.2 on 2023-11-04 18:15

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
