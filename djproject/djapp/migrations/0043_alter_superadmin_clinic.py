# Generated by Django 3.2.18 on 2023-04-02 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0042_alter_clinic_telnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superadmin',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clinic_superadmin', to='djapp.clinic'),
        ),
    ]
