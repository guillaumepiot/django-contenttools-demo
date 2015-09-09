# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20150909_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='edited_width',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
