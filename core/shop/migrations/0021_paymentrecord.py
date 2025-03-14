# Generated by Django 4.2.8 on 2025-03-13 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_alter_instructormonthlyincome_pay_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('description', models.CharField(max_length=250)),
                ('creted_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
