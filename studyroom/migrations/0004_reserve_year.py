# Generated by Django 3.1.3 on 2021-11-30 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyroom', '0003_auto_20211127_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='year',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
