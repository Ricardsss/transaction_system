# Generated by Django 5.1.3 on 2024-11-26 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(blank=True, default=236334790638, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(blank=True, choices=[('savings', 'Savings'), ('checking', 'Checking'), ('loan', 'Loan')], default='savings', max_length=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='account',
            name='currency',
            field=models.CharField(blank=True, default='CAD', max_length=3),
        ),
    ]
