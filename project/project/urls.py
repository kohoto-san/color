"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from os import environ

from apps.core import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^profile/(?P<id_profile>\d+)/$', views.profile_details, name='profile_details'),
    url(r'^profile/(?P<id_profile>\d+)/likes/$', views.profile_likes, name='profile_likes'),

    url(r'^$', views.load_home, name='home'),

    # url(r'^get', views.load_palettes, name='load_palettes'),

    url(r'^like/(?P<palette_id>\d+)/$', views.like, name='like'),

    url(r'^blend/$', views.blend, name='blend'),
    url(r'^blend-create/$', views.blend_create, name='blend_create'),

    url(r'^featured/(?P<blend_id>\d+)/$', views.featured_blend, name='featured_blend'),
    url(r'^p/(?P<blend_id>\d+)/$', views.blend_details, name='blend_details'),
]

if environ['DEBUG_BOOL']:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
