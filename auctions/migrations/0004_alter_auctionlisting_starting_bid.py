# Generated by Django 5.1.1 on 2024-09-21 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctionlisting_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]