# Generated by Django 3.1.2 on 2020-11-14 15:37

from django.db import migrations
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_exchange', '0004_auto_20201114_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='description',
            field=djrichtextfield.models.RichTextField(),
        ),
    ]
