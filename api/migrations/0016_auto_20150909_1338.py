# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20150909_1257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='edited_rotate',
            new_name='edited_direction',
        ),
    ]
