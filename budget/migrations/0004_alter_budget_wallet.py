# Generated by Django 5.1.4 on 2025-06-20 04:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_budget_wallet'),
        ('wallet', '0003_wallet_expired_date_alter_wallet_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='wallet',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='budget', to='wallet.wallet'),
        ),
    ]
