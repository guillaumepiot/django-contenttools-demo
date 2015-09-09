from django.conf.urls import patterns, include, url
from django.contrib import admin

from api import views, upload_views

urlpatterns = patterns('',
	url(r'^add/$', views.ContentHTMLAdd.as_view(), name='add'),
	url(r'^retrieve/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', views.ContentHTMLRetrieve.as_view(), name="retrieve"),
	url(r'^update/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', views.ContentHTMLUpdate.as_view(), name='update'),
	url(r'^list/$', views.ContentHTMLList.as_view(), name="list"),
	url(r'^delete/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', views.ContentHTMLDelete.as_view(), name="delete"),

	url(r'^images/add/$', upload_views.ImagesAdd.as_view(), name='images_add'),
	url(r'^images/update/(?P<id>[-\d]+)/$', upload_views.ImagesUpdate.as_view(), name='images_update'),
	url(r'^images/list/$', upload_views.ImagesList.as_view(), name='images_list'),

	url(r'^files/add/$', upload_views.FileUploadAdd.as_view(), name='file_add'),
)

