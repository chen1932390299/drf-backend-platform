# Generated by Django 3.2.2 on 2021-08-03 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0041_auto_20210803_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roleinfo',
            name='role_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]