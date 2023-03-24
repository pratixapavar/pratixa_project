# Generated by Django 4.1.4 on 2023-03-09 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('gst_no', models.CharField(max_length=15)),
                ('address', models.TextField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('pic', models.FileField(default='sad.jpg', upload_to='profile_pics')),
            ],
        ),
    ]
