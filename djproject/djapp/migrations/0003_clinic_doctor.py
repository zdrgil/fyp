# Generated by Django 3.2.18 on 2023-03-24 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0002_auto_20230324_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djapp.doctor'),
        ),
    ]