# Generated by Django 3.2.2 on 2021-06-05 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0019_testcase_error_msg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='runsuiterecord',
            old_name='case_ids',
            new_name='suite_ids',
        ),
    ]
