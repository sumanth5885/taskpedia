# Generated by Django 3.2.8 on 2023-08-27 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_assignments'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignments',
            name='valued',
            field=models.BooleanField(default=False),
        ),
    ]