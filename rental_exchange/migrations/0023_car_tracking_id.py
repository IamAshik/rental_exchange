# Generated by Django 3.1.2 on 2020-12-12 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_exchange', '0022_auto_20201210_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
