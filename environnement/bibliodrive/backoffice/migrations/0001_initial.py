# Generated by Django 5.1.2 on 2024-10-16 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('au_id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=50)),
                ('year_born', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('pubid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=10)),
                ('zip_code', models.CharField(max_length=15)),
                ('telephone', models.CharField(max_length=15)),
                ('fax', models.CharField(max_length=15)),
                ('comments', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('title', models.CharField(max_length=255)),
                ('year_published', models.SmallIntegerField()),
                ('isbn', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('notes', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=50)),
                ('comments', models.TextField()),
                ('pubid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.publisher')),
            ],
        ),
        migrations.CreateModel(
            name='TitleAuthor',
            fields=[
                ('isbn', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('au_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.author')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('isbn', 'au_id'), name='unique_title_author')],
            },
        ),
    ]
