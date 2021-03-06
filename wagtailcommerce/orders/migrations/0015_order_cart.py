# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-17 21:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcommerce_carts', '0004_cart_coupon'),
        ('wagtailcommerce_orders', '0014_auto_20180130_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='wagtailcommerce_carts.Cart', verbose_name='cart'),
        ),
    ]
