# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150909_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='size',
            field=models.CharField(default=b'', max_length=10, null=True, blank=True),
        ),
    ]
