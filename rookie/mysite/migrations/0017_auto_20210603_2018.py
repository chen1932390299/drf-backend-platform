# Generated by Django 3.2.2 on 2021-06-03 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0016_variablesglobal'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsuite',
            name='suite_name',
            field=models.CharField(default='0', max_length=50),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='case_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
