import json

from rest_framework import generics, permissions, filters

from rest_framework.parsers import FormParser, MultiPartParser
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

class ContentHTMLAdd(ContentHTMLMixin, generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        
        regions = self.request.data.get('regions')
        images = self.request.data.get('images')
        page = self.request.data.get('page')

        obj = serializer.save(
            regions = regions,
            images = images,
            page = page,
            )


class ContentHTMLRetrieve(ContentHTMLMixin, generics.RetrieveAPIView):
    lookup_field = 'uuid'


class ContentHTMLUpdate(ContentHTMLMixin, generics.UpdateAPIView):
    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()


class ContentHTMLList(ContentHTMLMixin, generics.ListAPIView):
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('created')
    ordering = ('-created',)


class ContentHTMLDelete(ContentHTMLMixin, generics.DestroyAPIView):
    lookup_field = 'uuid'

