"""quicklic_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from quicklic_backend.settings import STATIC_ROOT, MEDIA_ROOT
from website import urls as website_urls
from api.v1 import urls as v1_urls
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(website_urls, namespace="website")),
    url(r'^api/v1/', include(v1_urls)),
]

urlpatterns += [
    url(r'^static/(.*)$', serve, {'document_root': STATIC_ROOT, 'show_indexes': True}),
    url(r'^media/(.*)$', serve, {'document_root': MEDIA_ROOT, 'show_indexes': True})
]

