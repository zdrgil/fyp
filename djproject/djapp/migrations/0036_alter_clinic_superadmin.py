# Generated by Django 3.2.18 on 2023-04-01 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0035_auto_20230401_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='superadmin',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='superadmin_clinic', to='djapp.superadmin'),
        ),
    ]