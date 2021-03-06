# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-17 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcommerce_promotions', '0005_auto_20180317_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='added_to_cart',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='coupon_mode',
            field=models.CharField(choices=[('fixed', 'Fixed amount'), ('percentage', 'Percentage')], max_length=20, verbose_name='coupon mode'),
        ),
    ]
