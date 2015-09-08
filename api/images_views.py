import json

from rest_framework import generics
from rest_framework import permissions

from api.serializers import ImagesSerializer
from api.models import Images

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
        print self.request.data
        obj = serializer.save()

class ImagesList(ImagesMixin, generics.ListAPIView):
    pass