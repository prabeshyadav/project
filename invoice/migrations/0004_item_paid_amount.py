# Generated by Django 5.1.1 on 2024-09-14 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_alter_item_customer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='paid_amount',
            field=models.IntegerField(default=0),
        ),
    ]
