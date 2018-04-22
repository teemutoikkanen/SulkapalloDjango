"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from user import views as user_views
from rest_framework.authtoken import views as rest_views
from rest_framework.urlpatterns import format_suffix_patterns
from ilmoitukset import views as ilmo_views
from django.views.decorators.csrf import csrf_exempt
from haasteet import views as haaste_views
from matsit import views as matsi_views
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# See https://docs.djangoproject.com/en/2.0/topics/http/urls/
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^login/', rest_views.obtain_auth_token),
	url(r'^userlist/', user_views.UserViewSet),
    url(r'^register/', user_views.register),
	url(r'^users/(?P<id>[0-9]+)$', user_views.user_info), 
	url(r'^ilmoitukset/', csrf_exempt(ilmo_views.IlmoitusList.as_view())),
	url(r'^userilmoitukset/', csrf_exempt(ilmo_views.IlmoitusDetail.as_view())),
    url(r'^haastelista/', csrf_exempt(haaste_views.IlmonHaasteList.as_view())),
    url(r'^luohaaste/(?P<ilmo_id>[0-9]+)$', csrf_exempt(haaste_views.LuoHaaste.as_view())),
    url(r'^kayttajanhaasteet/', csrf_exempt(haaste_views.UserHaasteDetail.as_view())),
    url(r'^matsi/(?P<haaste_id>[0-9]+)$', csrf_exempt(matsi_views.MatsiAPI.as_view())),
    url(r'^deletehaaste/(?P<id>[0-9]+)$', csrf_exempt(haaste_views.DelHaaste.as_view())),
    url(r'^kmatsit/$', csrf_exempt(matsi_views.MatsiGET.as_view())),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
