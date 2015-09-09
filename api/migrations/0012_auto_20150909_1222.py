# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_images_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='width',
            new_name='edited_width',
        ),
        migrations.RenameField(
            model_name='images',
            old_name='url',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='images',
            name='size',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
