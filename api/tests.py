# -*- coding: utf-8 -*-
import os, json

from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import ContentHTML

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

		url = reverse('api:add')
		article = '''
		<h1>\n    5 rules for naming variables\n</h1>\n
		<p class=\"article__by-line\">\n    by <b>Anthony Blackshaw</b> · 
		18th January 2015\n</p>\n
		'''
		author = '''
		<h3 class=\"author__about\">\n    About the author\n</h3>\n
		<img alt=\"Anthony Blackshaw\" class=\"[ author__pic ]  [ align-right ]\" 
		height=\"80\" src=\"/static/author-pic.jpg\" width=\"80\">\n
		<p class=\"author__bio\">\n    
		Anthony Blackshaw is a co-founder of Getme, an employee owned company with a focus on web tech. 
		He enjoys writing and talking about tech, especially code and the occasional Montecristo No.2s.\n</p>
		'''
		learn = '''<h3>\n    Want to learn more?\n</h3>\n
		   <p>\n    If you'd like to learn more about the ContentTools library that makes this page editable, 
		   <a href=\"https://bitbucket.org/getmeuk/contenttools\">visit the projects homepage.</a>\n</p>
		   '''
		   
		data = {  
		   "article": article,
		   "author":author,
		   "learn-more":learn
		}

		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		print response.data['json']['article']
		self.assertEqual(response.data['json']['article'], u"%s" % article.decode("UTF-8"))
		self.assertEqual(response.data['json']['author'], u"%s" % author.decode("UTF-8"))
		self.assertEqual(response.data['json']['learn-more'], u"%s" % learn.decode("UTF-8"))

		object_id = response.data['uuid']

		# Retrieve
		url = reverse('api:retrieve', args=[object_id])
		
		response = self.client.get(url, format='json')
		self.assertEqual(response.data['json']['article'], u"%s" % article.decode("UTF-8"))
		self.assertEqual(response.data['json']['author'], u"%s" % author.decode("UTF-8"))
		self.assertEqual(response.data['json']['learn-more'], u"%s" % learn.decode("UTF-8"))

		self.assertEqual(response.status_code, status.HTTP_200_OK)

