# Generated by Django 3.2.6 on 2021-10-11 18:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stats_api', '0006_auto_20211011_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='join_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
