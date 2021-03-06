# Generated by Django 3.2.2 on 2021-08-02 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0039_auto_20210802_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=50)),
                ('role_type', models.CharField(choices=[('0', '普通角色'), ('1', '管理员')], max_length=10)),
                ('status', models.CharField(choices=[('0', '禁用'), ('1', '启用')], max_length=10)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tbl_role_info',
                'ordering': ['-create_time'],
            },
        ),
    ]
