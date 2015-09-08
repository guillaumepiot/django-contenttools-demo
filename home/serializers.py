import json

from rest_framework import serializers
from api.models import ContentHTML

class ContentHTMLSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentHTML
        fields = ('id',
                  'uuid',
                  'json')

    def to_representation(self, instance):
        ret = super(ContentHTMLSerializer, self).to_representation(instance)
        ret['json'] = json.loads(ret['json'])
        return ret

    def validate(self, data):
        return data
