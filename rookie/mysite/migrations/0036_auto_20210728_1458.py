# Generated by Django 3.2.2 on 2021-07-28 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0035_taskexcuterecord'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='runsuiterecord',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='taskexcuterecord',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelTable(
            name='taskexcuterecord',
            table='tbl_task_execute_record',
        ),
    ]
