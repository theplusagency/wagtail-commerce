# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-23 14:19
from __future__ import unicode_literals

from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcommerce_orders', '0016_auto_20180221_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_cost_tax',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_cost_total',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12, verbose_name='shipping cost total'),
            preserve_default=False,
        ),
    ]
