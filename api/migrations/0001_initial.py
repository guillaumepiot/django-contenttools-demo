# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentHTML',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('images', models.CharField(null=True, blank=True, max_length=100)),
                ('page', models.CharField(null=True, blank=True, max_length=100)),
                ('regions', models.TextField(null=True, blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datafile', models.FileField(upload_to='files')),
                ('owner', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(null=True, upload_to='images')),
                ('name', models.CharField(null=True, blank=True, max_length=100)),
                ('edited_width', models.IntegerField(null=True, blank=True)),
                ('edited_crop', models.CharField(null=True, blank=True, max_length=15)),
                ('edited_direction', models.CharField(null=True, blank=True, max_length=5)),
            ],
        ),
    ]
