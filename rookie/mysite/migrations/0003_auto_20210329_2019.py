# Generated by Django 2.2.17 on 2021-03-29 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_auto_20210329_2016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookrelatedauthor',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='bookrelatedauthor',
            old_name='book_id',
            new_name='book',
        ),
    ]
