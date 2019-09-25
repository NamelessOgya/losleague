# Generated by Django 2.2.5 on 2019-09-23 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0017_deckcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='deckcode',
            name='match',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='match', to='attendance.Match'),
        ),
    ]