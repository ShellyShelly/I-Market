# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20171021_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, upload_to='shop', verbose_name='Зображення книги'),
        ),
    ]
