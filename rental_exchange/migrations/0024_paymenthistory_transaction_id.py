# Generated by Django 3.1.2 on 2020-12-14 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_exchange', '0023_car_tracking_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
