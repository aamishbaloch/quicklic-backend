from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list', views.DoctorView.as_view(), name='doctor-list'),
]
