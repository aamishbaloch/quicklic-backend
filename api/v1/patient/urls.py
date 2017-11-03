from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[\d]+)$', views.PatientView.as_view()),
    url(r'^$', views.PatientListView.as_view()),
    url(r'^clinic/$', views.PatientClinicView.as_view()),
    url(r'^clinic/(?P<clinic_id>[\d]+)', views.PatientClinicView.as_view()),
    url(r'^doctor/(?P<doctor_id>[\d]+)/clinic/', views.PatientDoctorClinicView.as_view()),
]
