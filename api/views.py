import json

from rest_framework import generics
from rest_framework import permissions

from api.serializers import ContentHTMLSerializer
from api.models import ContentHTML, Images

#
# Mixin for all company views.
# Defines serializers, queryset and permissions
#

class ContentHTMLMixin(object):

    def get_queryset(self):
        return ContentHTML.objects.filter()

    def get_serializer_class(self):
        return ContentHTMLSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

class ContentHTMLAdd(ContentHTMLMixin, generics.CreateAPIView):
    def perform_create(self, serializer):
        print self.request.user
        data = json.dumps(self.request.data)
        obj = serializer.save(json = data)


class ContentHTMLRetrieve(ContentHTMLMixin, generics.RetrieveAPIView):
    lookup_field = 'uuid'


class ContentHTMLUpdate(ContentHTMLMixin, generics.UpdateAPIView):
    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()


class ContentHTMLList(ContentHTMLMixin, generics.ListAPIView):
    pass


class ContentHTMLDelete(ContentHTMLMixin, generics.DestroyAPIView):
    lookup_field = 'uuid'

