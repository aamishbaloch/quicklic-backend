from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all/', views.DoctorView.as_view(), name='doctor-all'),
]
