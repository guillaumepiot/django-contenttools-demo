from django.db import models
import uuid
from django.contrib.auth.models import User

class ContentHTML(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    images = models.CharField(max_length=100, blank=True, null=True)
    page = models.CharField(max_length=100, blank=True, null=True)
    regions = models.TextField(blank=True, default='', null=True)
    

class Images(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, max_length=100, null=True)
    name =  models.CharField(max_length=100, blank=True, null=True)

    edited_width = models.IntegerField(blank=True, null=True)
    edited_crop = models.CharField(max_length=15, blank=True, null=True)
    edited_direction = models.CharField(max_length=5, blank=True, null=True)

    def size(self):
        return [self.image.width, self.image.height]

    # def rotate(self):

    #         if not self.id and not self.image:
    #             return            

    #         super(Images, self).save()

    #         path_image = cStringIO.StringIO(urllib.urlopen(self.image).read())
    #         print path_image
    #         im.rotate(90)


    #         image = Image.open(path_image)

    #         image.resize(size, Image.ANTIALIAS)
    #         image.save(self.photo.path)
class FileUpload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, null=True)
    datafile = models.FileField(upload_to='files')