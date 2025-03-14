# Generated by Django 4.2.8 on 2025-03-13 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_instructor_share_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructormonthlyincome',
            name='is_payed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='instructormonthlyincome',
            name='pay_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
