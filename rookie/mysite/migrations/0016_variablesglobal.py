# Generated by Django 3.2.2 on 2021-06-01 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0015_auto_20210531_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariablesGlobal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('variable_value', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
