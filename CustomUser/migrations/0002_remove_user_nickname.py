# Generated by Django 3.1.3 on 2022-01-18 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
    ]
