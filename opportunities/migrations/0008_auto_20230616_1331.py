# Generated by Django 3.2.9 on 2023-06-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('opportunities', '0007_auto_20230616_1256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opportunity',
            options={'ordering': ('-last_updated',), 'verbose_name_plural': 'opportunities'},
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='abstract',
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='location',
            field=models.ManyToManyField(null=True, to='common.Location'),
        ),
    ]
