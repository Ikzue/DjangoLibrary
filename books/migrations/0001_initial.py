# Generated by Django 4.2 on 2023-10-24 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('isbn', models.CharField(max_length=17)),
                ('release_date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authors.author')),
                ('co_authors', models.ManyToManyField(blank=True, related_name='coauthors', to='authors.author')),
            ],
        ),
    ]
