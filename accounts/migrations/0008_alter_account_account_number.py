# Generated by Django 5.1.3 on 2024-11-27 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_account_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(blank=True, default=767983986767, max_length=12, unique=True),
        ),
    ]
