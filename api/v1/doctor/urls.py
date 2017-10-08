from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.DoctorView.as_view()),
    url(r'^list', views.DoctorListView.as_view(), name='doctor-list'),
]
