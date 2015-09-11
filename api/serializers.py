import json
from rest_framework import serializers
from api.models import ContentHTML, Images, FileUpload

class ContentHTMLSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentHTML
        fields = ('id',
                  'created',  
                  'uuid',
                  'page',
                  'regions',
                  'images')

    def to_representation(self, instance):
        ret = super(ContentHTMLSerializer, self).to_representation(instance)
        ret['regions'] = json.loads(ret['regions'])
        return ret

    def validate(self, data):
        return data

class ImagesSerializer(serializers.ModelSerializer):

    size = serializers.ListField(
        read_only=True,
        child=serializers.IntegerField()
    )

    # edited_width = serializers.IntegerField(
    #     write_only = True,
    #     required = False
    #     )
    # edited_crop = serializers.ListField(
    #     write_only = True,
    #     child=serializers.IntegerField(),
    #     required = False
    #     )
    # edited_direction = serializers.CharField(
    #     write_only = True,
    #     required = False

    #     )


    class Meta:
        model = Images
        fields = ('id',
                  'created',
                  'image',
                  'name',
                  'size',

                  'edited_width',
                  'edited_crop',
                  'edited_direction',
                  )


    def to_representation(self, instance):
        ret = super(ImagesSerializer, self).to_representation(instance)
        # ret['size'] = ret['size']
        return ret


class FileUploadSerializer(serializers.ModelSerializer):
    # owner = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='id'
    # )

    class Meta:
        model = FileUpload
        fields = ('created', 'datafile', 'owner')



