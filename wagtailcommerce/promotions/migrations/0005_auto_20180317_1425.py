# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-17 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcommerce_promotions', '0004_auto_20180129_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='product_variants',
        ),
        migrations.AddField(
            model_name='coupon',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified on'),
        ),
    ]
