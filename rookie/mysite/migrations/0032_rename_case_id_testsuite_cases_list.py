# Generated by Django 3.2.2 on 2021-06-19 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0031_auto_20210615_1725'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testsuite',
            old_name='case_id',
            new_name='cases_list',
        ),
    ]