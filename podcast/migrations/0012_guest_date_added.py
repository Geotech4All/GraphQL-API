# Generated by Django 3.2.9 on 2023-01-15 16:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0011_rename_opportuinity_opportunity'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
