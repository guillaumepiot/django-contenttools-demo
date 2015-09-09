from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from home import views

urlpatterns = patterns('',
    url(r'^$', views.home_view, name='home_view'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})
)

