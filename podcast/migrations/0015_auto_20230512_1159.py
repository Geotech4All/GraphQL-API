# Generated by Django 3.2.9 on 2023-05-12 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0008_auto_20230512_0625'),
        ('podcast', '0014_delete_opportunity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='audio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.file'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='cover_photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.image'),
        ),
    ]
