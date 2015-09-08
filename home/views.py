import json

from django.shortcuts import render_to_response
from django.http import HttpResponse

from django.template import RequestContext, loader

from api.models import ContentHTML

def home_view(request):
	template = loader.get_template('home.html')
	# Get only the last log created
	content = ContentHTML.objects.latest('created')
	# We only want the field in Model called json
	content = content.json
	context = RequestContext(request,json.loads(content))

	return HttpResponse(template.render(context))
