# -*- coding: utf-8 -*-
import os, json
from urlparse import urlparse

from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.files.base import ContentFile
from api.models import ContentHTML, FileUpload

# Create your tests here.
class ContentHTMLTests(APITestCase):


	def test_add(self):

		""" Test if we can add, retrieve and list """

		#
		# Login
		#

		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

		token = Token.objects.create(user=user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		# Make sure we can get the token back from that user
		self.token = Token.objects.get(user=user)
		self.assertEqual(token, self.token)

		#
		# Save Changes
		#
					# 'regions' : {  
			#    "article": article,
			#    "author":author,
			#    "learn-more":learn
			# }


		url = reverse('api:add')
		article = '''
		<h1>\n    5 rules for naming variables\n</h1>\n
		<p class=\"article__by-line\">\n    by <b>Anthony Blackshaw</b> · 
		18th January 2015\n</p>\n
		'''

	  	data = {u'images': [u'{}'], 
	  	u'regions': [u'''{
	  	"article": "<h3 class=\"author__about\">\n    About the author\n</h3>\n
		<img alt=\"Anthony Blackshaw\" class=\"[ author__pic ]  [ align-right ]\" 
		height=\"80\" src=\"/static/author-pic.jpg\" width=\"80\">\n
		<p class=\"author__bio\">\n    
		Anthony Blackshaw is a co-founder of Getme, an employee owned company with a focus on web tech. 
		He enjoys writing and talking about tech, especially code and the occasional Montecristo No.2s.\n</p>"}'''],
	  	u'page': [u'/']
	  	}
	  	

		response = self.client.post(url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		object_id = response.data['uuid']

		# Retrieve
		url = reverse('api:retrieve', args=[object_id])
		
		response = self.client.get(url, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class ImageUploadTests(APITestCase):

	def test_upload_image(self):
		from StringIO import StringIO
		from PIL import Image

		#
		# Login
		#

		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

		token = Token.objects.create(user=user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		# Make sure we can get the token back from that user
		self.token = Token.objects.get(user=user)
		self.assertEqual(token, self.token)

		#
		# Upload Image
		#

		url = reverse('api:images_add')

		file_obj = StringIO()
		image    = Image.new("RGBA", size=(50,50), color=(256,0,0))
		image.save(file_obj, 'png')
		file_obj.name = 'test.png'
		file_obj.seek(0)
		django_friendly_file = ContentFile(file_obj.read(), 'test.png')

		data = {u'width': [u'600'], u'image': django_friendly_file}

		# Upload a file with an authenticated user
		response = self.client.post(url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('created', response.data)

		image_id = response.data['id']


		#
		# Update Image
		#

		url = reverse('api:images_update', args=[image_id])

		# Crop Image
		data = {u'crop': [u'0,0,1,1']}
		response = self.client.post(url, data, format='multipart')

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# assert unauthenticated user can not upload file
		self.client.logout()
		response = self.client.post(url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FileUploadTests(APITestCase):

	def _create_test_file(self, path):
		f = open(path, 'w')
		f.write('test123\n')
		f.close()
		f = open(path, 'rb')
		return {'datafile': f}

	def test_upload_file(self):
		url = reverse('api:file_add')
		data = self._create_test_file('/tmp/test_upload')

		#
		# Login
		#

		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

		token = Token.objects.create(user=user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		# Make sure we can get the token back from that user
		self.token = Token.objects.get(user=user)
		self.assertEqual(token, self.token)

		# Upload a file with an authenticated user
		response = self.client.post(url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('created', response.data)
		self.assertTrue(urlparse(
			response.data['datafile']).path.startswith(settings.MEDIA_URL))
		self.assertIn('created', response.data)

		# assert unauthenticated user can not upload file
		self.client.logout()
		response = self.client.post(url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)