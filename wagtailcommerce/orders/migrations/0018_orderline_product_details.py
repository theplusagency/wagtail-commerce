# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-01 02:55
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcommerce_orders', '0017_auto_20180223_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='product_details',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]
