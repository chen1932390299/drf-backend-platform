# Generated by Django 3.2.2 on 2021-06-15 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0029_auto_20210615_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '项目配置表',
                'db_table': 'tbl_project_config',
                'ordering': ['id'],
            },
        ),
    ]
