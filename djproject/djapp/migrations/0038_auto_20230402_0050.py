# Generated by Django 3.2.18 on 2023-04-01 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0037_auto_20230402_0023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin',
            options={'permissions': [('can_manage_clinic', "Can manage self's clinic"), ('can_manage_customer', 'Can manage customer'), ('can_manage_doctor', 'Can manage doctor'), ('can_manage_appointment', 'Can manage appointment')]},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'permissions': [('can_manage_appointment', 'Can manage appointment')]},
        ),
    ]
