from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list', views.PatientView.as_view(), name='patient-list'),
]
