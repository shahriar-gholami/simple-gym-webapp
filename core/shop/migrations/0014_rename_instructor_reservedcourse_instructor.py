# Generated by Django 4.2.8 on 2025-03-12 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_salarypayment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservedcourse',
            old_name='Instructor',
            new_name='instructor',
        ),
    ]
