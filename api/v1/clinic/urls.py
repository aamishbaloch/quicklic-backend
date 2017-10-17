from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ClinicView.as_view()),
    url(r'^add/patient/$', views.AddPatientToClinicView.as_view()),
]
