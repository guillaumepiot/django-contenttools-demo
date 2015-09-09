# -*- coding: utf-8 -*-
import json, ast

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader

from api.models import ContentHTML



def home_view(request):
	template = loader.get_template('home.html')
	# Get only the last log created
	if (ContentHTML.objects.all()):
		content = ContentHTML.objects.latest('created')
		regions = json.loads(content.regions).encode('utf-8')
		regions = json.loads(regions)
		print type(regions)
		context = RequestContext(request, regions)
	else:
		context = RequestContext(request, {})
	return HttpResponse(template.render(context))
