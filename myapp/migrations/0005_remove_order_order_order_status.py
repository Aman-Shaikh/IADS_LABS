# Generated by Django 5.0.6 on 2024-07-13 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_order_order_date_order_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Purchased', 'Purchased'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Purchased', max_length=10),
        ),
    ]
