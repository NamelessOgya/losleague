# Generated by Django 2.2.5 on 2019-09-16 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0013_classwinrate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classwinrate',
            old_name='b',
            new_name='lose',
        ),
        migrations.RenameField(
            model_name='classwinrate',
            old_name='d',
            new_name='rate',
        ),
        migrations.RenameField(
            model_name='classwinrate',
            old_name='e',
            new_name='win',
        ),
        migrations.RemoveField(
            model_name='classwinrate',
            name='nc',
        ),
        migrations.RemoveField(
            model_name='classwinrate',
            name='nm',
        ),
        migrations.RemoveField(
            model_name='classwinrate',
            name='r',
        ),
        migrations.RemoveField(
            model_name='classwinrate',
            name='v',
        ),
        migrations.RemoveField(
            model_name='classwinrate',
            name='w',
        ),
        migrations.AddField(
            model_name='classwinrate',
            name='leader',
            field=models.CharField(default='', max_length=100),
        ),
    ]
