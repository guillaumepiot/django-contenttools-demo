# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20150909_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='size',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
