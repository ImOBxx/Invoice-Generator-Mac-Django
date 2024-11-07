# Generated by Django 5.1.2 on 2024-11-07 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0003_invoice_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
