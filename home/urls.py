from django.conf.urls import patterns, include, url
from django.contrib import admin

from home import views

urlpatterns = patterns('',
    url(r'^$', views.home_view, name='home_view'),
)

