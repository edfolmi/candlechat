# Generated by Django 4.2.4 on 2023-08-10 16:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Messages',
            new_name='GroupBlock',
        ),
    ]
