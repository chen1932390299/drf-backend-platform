# Generated by Django 3.2.3 on 2021-05-25 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0013_alter_vuemodel_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='assert_express',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='testcase',
            name='extract',
            field=models.JSONField(null=True),
        ),
    ]
