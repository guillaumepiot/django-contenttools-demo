import json, urllib, cStringIO, re, os

from rest_framework import generics, permissions, filters
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from api.serializers import ImagesSerializer, FileUploadSerializer
from api.models import Images, FileUpload
from django.conf import settings
from PIL import Image

#
# Mixin for all company views.
# Defines serializers, queryset and permissions
#

class ImagesMixin(object):

	def get_queryset(self):
		return Images.objects.filter()

	def get_serializer_class(self):
		return ImagesSerializer

	def get_permissions(self):
		return [permissions.IsAuthenticated()]

class ImagesAdd(ImagesMixin, generics.CreateAPIView):
	def perform_create(self, serializer):
		obj = serializer.save(
			image = self.request.data['image'], 
			name = self.request.data['image'].name,
			edited_width = self.request.data['width'])

class ImagesList(ImagesMixin, generics.ListAPIView):
	filter_backends = (filters.OrderingFilter,)
	ordering_fields = ('created')
	ordering = ('-created',)

class ImagesUpdate(ImagesMixin, generics.UpdateAPIView):
	lookup_field = 'id'
	def post(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def perform_update(self, serializer):
		print self.request.data
		if self.request.data.get('crop'):
			serializer.save(
				edited_crop = self.request.data['crop'],
				)
		if self.request.data.get('direction'):
			angle = 270 if self.request.data['direction'] == "CW" else 90
			url_image = serializer.data.get('image')
			path_image = cStringIO.StringIO(urllib.urlopen(url_image).read())

			im = Image.open(path_image)

			im = im.rotate(angle)
			path = re.match('^(.*)/([^/]*)$', url_image)

			im.save( settings.MEDIA_ROOT + 'images/' + path.group(2))

			serializer.save(edited_direction = self.request.data['direction'])




class FileUploadMixin(object):

	def get_queryset(self):
		return FileUpload.objects.all()

	def get_serializer_class(self):
		return FileUploadSerializer

	def get_permissions(self):
		return [permissions.IsAuthenticated()]

class FileUploadAdd(FileUploadMixin, generics.CreateAPIView):

	parser_classes = (MultiPartParser, FormParser,)

	def perform_create(self, serializer):
		serializer.save()