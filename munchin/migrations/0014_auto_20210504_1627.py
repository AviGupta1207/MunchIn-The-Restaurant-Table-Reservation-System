# Generated by Django 3.1.4 on 2021-05-04 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('munchin', '0013_foodorder_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodorder',
            old_name='status',
            new_name='Completed',
        ),
        migrations.AddField(
            model_name='foodorder',
            name='cvv',
            field=models.CharField(default='', max_length=3),
        ),
        migrations.AddField(
            model_name='foodorder',
            name='debitcard',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AddField(
            model_name='foodorder',
            name='expiry',
            field=models.CharField(default='', max_length=5),
        ),
    ]
