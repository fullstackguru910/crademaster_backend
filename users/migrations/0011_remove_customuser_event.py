# Generated by Django 5.1.4 on 2025-02-06 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_customuser_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='event',
        ),
    ]
