# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-23 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcommerce_products', '0017_auto_20180221_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='active',
            field=models.BooleanField(verbose_name='active'),
        ),
    ]
