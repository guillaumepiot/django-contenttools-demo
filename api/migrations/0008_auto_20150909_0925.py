# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150909_0836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contenthtml',
            old_name='json',
            new_name='regions',
        ),
        migrations.AddField(
            model_name='contenthtml',
            name='images',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contenthtml',
            name='page',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
