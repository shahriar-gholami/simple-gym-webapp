# Generated by Django 4.2.8 on 2025-03-14 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_alter_reservedcourse_register_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='instructor',
            name='birthday',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='instructor',
            name='study',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
