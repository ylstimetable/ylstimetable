# Generated by Django 3.1.3 on 2021-02-08 12:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('professor', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=200)),
                ('room', models.CharField(max_length=200)),
                ('semester', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=200)),
                ('ban', models.CharField(max_length=200)),
                ('voter', models.ManyToManyField(blank=True, related_name='class_voter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
