# Generated by Django 3.2.13 on 2022-05-17 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_auto_20220511_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.DateField(default=datetime.date(2022, 5, 17)),
        ),
    ]
