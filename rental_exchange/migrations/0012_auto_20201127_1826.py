# Generated by Django 3.1.2 on 2020-11-27 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_exchange', '0011_auto_20201127_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carbooking',
            name='customer',
        ),
        migrations.AlterField(
            model_name='carbooking',
            name='is_seen',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='carbooking',
            name='payment_status',
            field=models.CharField(blank=True, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', max_length=50),
        ),
        migrations.AlterField(
            model_name='carbooking',
            name='request_status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=50),
        ),
    ]
