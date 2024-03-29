# Generated by Django 3.2.9 on 2023-04-08 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('category', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
