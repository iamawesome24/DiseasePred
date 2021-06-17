# Generated by Django 3.2.2 on 2021-05-18 19:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_app', '0005_auto_20210518_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.CharField(default=datetime.datetime(2021, 5, 18, 19, 5, 41, 222621), max_length=100),
        ),
        migrations.AlterField(
            model_name='patient',
            name='last_interaction',
            field=models.DateField(default=datetime.datetime(2021, 5, 18, 19, 5, 41, 222744)),
        ),
    ]
