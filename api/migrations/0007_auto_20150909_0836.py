# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150909_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='datafile',
            field=models.FileField(upload_to=b'files'),
        ),
    ]
