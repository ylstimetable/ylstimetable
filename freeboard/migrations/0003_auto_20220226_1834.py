# Generated by Django 3.1.3 on 2022-02-26 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freeboard', '0002_post_delete_unavailable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='delete_unavailable',
            field=models.BooleanField(max_length=2, null=True),
        ),
    ]