# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20150909_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='edited_crop',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='images',
            name='edited_rotate',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
    ]
