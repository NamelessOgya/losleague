# Generated by Django 2.2.5 on 2019-09-16 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0014_auto_20190916_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='classwinrate',
            name='total',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=''),
        ),
    ]