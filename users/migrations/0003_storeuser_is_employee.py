# Generated by Django 3.1.1 on 2020-11-11 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201030_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeuser',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
    ]
