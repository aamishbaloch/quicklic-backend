from django.conf.urls import url, include
from api.v1.authentication import urls as auth_urls

urlpatterns = [
    url(r'^auth/', include(auth_urls)),
]