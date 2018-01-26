# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-26 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcommerce_orders', '0009_auto_20180126_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('payment_pending', 'Payment pending'), ('awaiting_payment_confirmation', 'Awaiting payment confirmation'), ('awaiting_payment_authorization', 'Awaiting payment authorization'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='payment_pending', max_length=30, verbose_name='status'),
        ),
    ]