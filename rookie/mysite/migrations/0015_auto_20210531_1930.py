# Generated by Django 3.2.2 on 2021-05-31 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0014_auto_20210525_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSuite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.JSONField()),
                ('status', models.CharField(default='0', max_length=20)),
            ],
            options={
                'verbose_name': '接口套件表',
                'db_table': 'tbl_test_suite',
            },
        ),
        migrations.AddField(
            model_name='testcase',
            name='status',
            field=models.CharField(default='0', max_length=20),
        ),
    ]