# Generated by Django 2.2.5 on 2019-09-13 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_auto_20190913_0624'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registered',
            old_name='fifthl',
            new_name='hoketsu',
        ),
        migrations.RemoveField(
            model_name='registered',
            name='fifthwl',
        ),
        migrations.RemoveField(
            model_name='registered',
            name='firstl',
        ),
        migrations.RemoveField(
            model_name='registered',
            name='firstwl',
        ),
        migrations.RemoveField(
            model_name='registered',
            name='fourthl',
        ),
        migrations.RemoveField(
            model_name='registered',
            name='fourthwl',
        ),
        migrations.RemoveField(
            model_name='registered',
            name='secondl',
        ),
        migrations.RemoveField(
            model_name='registered',
            name='secondwl',
        ),
        migrations.RemoveField(
            model_name='registered',
            name='thirdl',
        ),
        migrations.RemoveField(
            model_name='registered',
            name='thirdwl',
        ),
        migrations.CreateModel(
            name='Reported',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(default='', max_length=100)),
                ('first', models.CharField(default='', max_length=100)),
                ('second', models.CharField(default='', max_length=100)),
                ('third', models.CharField(default='', max_length=100)),
                ('fourth', models.CharField(default='', max_length=100)),
                ('fifth', models.CharField(default='', max_length=100)),
                ('firstl', models.CharField(default='', max_length=100)),
                ('secondl', models.CharField(default='', max_length=100)),
                ('thirdl', models.CharField(default='', max_length=100)),
                ('fourthl', models.CharField(default='', max_length=100)),
                ('fifthl', models.CharField(default='', max_length=100)),
                ('firstwl', models.CharField(default='', max_length=100)),
                ('secondwl', models.CharField(default='', max_length=100)),
                ('thirdwl', models.CharField(default='', max_length=100)),
                ('fourthwl', models.CharField(default='', max_length=100)),
                ('fifthwl', models.CharField(default='', max_length=100)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Match')),
            ],
        ),
    ]
