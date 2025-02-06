# Generated by Django 5.1.4 on 2025-02-06 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=30.0, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
