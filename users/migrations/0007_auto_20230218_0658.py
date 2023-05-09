# Generated by Django 3.2.9 on 2023-02-18 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20230105_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='can_alter_podcast',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='can_alter_post',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='can_alter_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='can_create_podcast',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='can_create_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='can_delete_podcast',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='can_delete_post',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='can_delete_user',
            field=models.BooleanField(default=False),
        ),
    ]
