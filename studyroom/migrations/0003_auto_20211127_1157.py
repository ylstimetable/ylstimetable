# Generated by Django 3.1.3 on 2021-11-27 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyroom', '0002_auto_20211120_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='day',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='reserve',
            name='month',
            field=models.CharField(max_length=200, null=True),
        ),
    ]