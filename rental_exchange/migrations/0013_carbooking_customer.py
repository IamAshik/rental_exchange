# Generated by Django 3.1.2 on 2020-11-27 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rental_exchange', '0012_auto_20201127_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='carbooking',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='users.user'),
            preserve_default=False,
        ),
    ]
