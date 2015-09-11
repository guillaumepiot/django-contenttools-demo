from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^', include('home.urls', namespace='home')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^admin/', include(admin.site.urls)),
)
