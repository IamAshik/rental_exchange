# Generated by Django 3.1.2 on 2020-11-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_exchange', '0019_auto_20201129_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionhistory',
            name='paid_date',
            field=models.DateTimeField(auto_now=True, default='2020-11-29 17:10:18.198277+06'),
            preserve_default=False,
        ),
    ]