# Generated by Django 5.1.1 on 2024-12-23 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_userinfo_registered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='registered',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
