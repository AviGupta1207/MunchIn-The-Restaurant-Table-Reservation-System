# Generated by Django 3.1.4 on 2021-04-28 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munchin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='uemail',
        ),
    ]
