# Generated by Django 3.2.9 on 2023-06-25 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('opportunities', '0009_auto_20230616_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opportunity',
            name='location',
        ),
        migrations.AddField(
            model_name='opportunity',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.location'),
        ),
    ]
