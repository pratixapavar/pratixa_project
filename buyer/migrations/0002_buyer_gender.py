# Generated by Django 4.1.4 on 2023-01-25 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]