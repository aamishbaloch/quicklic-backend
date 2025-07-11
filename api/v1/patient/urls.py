from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[\d]+)$', views.PatientView.as_view()),
    url(r'^$', views.PatientListView.as_view()),
    url(r'^(?P<pk>[\d]+)/clinic/$', views.PatientClinicView.as_view()),
    url(r'^(?P<pk>[\d]+)/clinic/(?P<clinic_id>[\d]+)$', views.PatientClinicView.as_view()),
    url(r'^(?P<pk>[\d]+)/doctor/(?P<doctor_id>[\d]+)/clinic/$', views.PatientDoctorClinicView.as_view()),
    url(r'^(?P<pk>[\d]+)/doctor/$', views.PatientDoctorsView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment/$', views.PatientAppointmentView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment/history$', views.PatientAppointmentHistoryView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment/(?P<appointment_id>[\d]+)/cancel/$', views.PatientAppointmentCancelView.as_view()),
    url(r'^(?P<pk>[\d]+)/visit/$', views.PatientVisitView.as_view()),
    url(r'^(?P<pk>[\d]+)/review/$', views.PatientReviewView.as_view()),
]
