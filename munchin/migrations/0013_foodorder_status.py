# Generated by Django 3.1.4 on 2021-05-04 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('munchin', '0012_auto_20210501_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodorder',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
