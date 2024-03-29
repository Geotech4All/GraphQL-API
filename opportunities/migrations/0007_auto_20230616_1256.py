# Generated by Django 3.2.9 on 2023-06-16 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('opportunities', '0006_auto_20230616_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='location',
            field=models.ManyToManyField(to='common.Location'),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.organization'),
        ),
    ]
