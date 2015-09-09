# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150909_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='url',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='images',
            name='width',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(null=True, upload_to=b'images'),
        ),
    ]
