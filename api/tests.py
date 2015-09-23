# -*- coding: utf-8 -*-
import os, json, io
from urllib.parse import urlparse
from PIL import Image

from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import ContentHTML, FileUpload

# Create your tests here.
class ContentHTMLTests(APITestCase):

    def setUp(self):
        # Add a default user and generate an authentication token
        self.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_add(self):

        """ Test if we can add, retrieve and list """

        #
        # Authenticate the client
        #
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create the add URL
        url = reverse('api:add')

        article = '''<h1>\n    5 rules for naming variables\n</h1>\n
            <p class=\"article__by-line\">\n    by <b>Anthony Blackshaw</b> · 
            18th January 2015\n</p>\n'''

        data = {
            'images': ['{}'], 
            'regions': ["""{"article": "<h3 class=\"author__about\">\n
                About the author\n</h3>\n
                <img alt=\"Anthony Blackshaw\" 
                    class=\"[ author__pic ]  [ align-right ]\" 
                height=\"80\" src=\"/static/author-pic.jpg\" width=\"80\">\n
                <p class=\"author__bio\">\n    
                Anthony Blackshaw is a co-founder of Getme, an employee owned 
                company with a focus on web tech. He enjoys writing and talking 
                about tech, especially code and the occasional 
                Montecristo No.2s.\n</p>"}"""
                ],
            'page': ['/']
        }
        

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        object_id = response.data['uuid']

        # Retrieve
        url = reverse('api:retrieve', args=[object_id])
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ImageUploadTests(APITestCase):

    def setUp(self):
        # Add a default user and generate an authentication token
        self.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
    def test_upload_image(self):

        #
        # Authenticate the client
        #
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        #
        # Upload Image
        #

        url = reverse('api:images_add')

        file_obj = io.BytesIO()
        image = Image.new("RGBA", size=(50,50), color=(256,0,0))
        image.save(file_obj, 'png')

        file_obj.seek(0)
        
        django_friendly_file = ContentFile(file_obj.read(), 'test.png')

        data = {
            'width': ['600'], 
            'image': django_friendly_file
            }

        # Upload a file with an authenticated user
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created', response.data)

        image_id = response.data['id']


        #
        # Crop Image
        #

        url = reverse('api:images_update', args=[image_id])

        data = {
            'crop': ['0,0,10,10']
            }
        
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert unauthenticated user can not upload file
        self.client.logout()
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
