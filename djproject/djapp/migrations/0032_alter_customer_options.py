# Generated by Django 3.2.18 on 2023-04-01 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0031_customer_phonenumber'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': [('view_customer_info', 'Can view customer information'), ('edit_customer_info', 'Can edit customer information'), ('delete_customer_info', 'Can delete customer information')]},
        ),
    ]