# Generated by Django 3.2.18 on 2023-04-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0041_alter_clinic_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='telnum',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
