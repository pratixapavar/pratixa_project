# Generated by Django 4.1.4 on 2023-03-21 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0003_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product_namen',
            new_name='product_name',
        ),
    ]
