# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20171018_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='media/None/no-img.jpg', upload_to='media', verbose_name='Зображення книги'),
        ),
    ]
