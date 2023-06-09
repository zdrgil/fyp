# Generated by Django 3.2.18 on 2023-03-30 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0015_remove_appointment_clinic'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='clinic',
            field=models.ForeignKey(limit_choices_to={'state': 'open'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='djapp.clinic'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='clinicname',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='djapp.clinic'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='sex',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
