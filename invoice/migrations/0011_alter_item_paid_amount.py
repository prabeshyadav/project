# Generated by Django 5.1.1 on 2025-01-03 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0010_alter_userinfo_registered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='paid_amount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
