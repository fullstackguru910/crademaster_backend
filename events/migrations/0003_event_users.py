# Generated by Django 5.1.4 on 2025-02-06 22:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(related_name='events', to=settings.AUTH_USER_MODEL),
        ),
    ]
