from django.db import models
import uuid

class ContentHTML(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    json = models.TextField(blank=True, default='', null=True)
    

class Images(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, max_length=100, null=True)
