from django.conf.urls import url, include
from api.v1.authentication import urls as auth_urls
from api.v1.doctor import urls as doctor_urls

urlpatterns = [
    url(r'^auth/', include(auth_urls)),
    url(r'^doctor/', include(doctor_urls)),
]