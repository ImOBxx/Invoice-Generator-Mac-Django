# Generated by Django 5.1.2 on 2024-11-07 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0002_invoice_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]