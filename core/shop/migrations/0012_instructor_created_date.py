# Generated by Django 4.2.8 on 2025-03-11 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_instructor_reservedcourse_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
