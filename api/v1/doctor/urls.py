from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[\d]+)$', views.DoctorView.as_view()),
    url(r'^$', views.DoctorListView.as_view()),
    url(r'^(?P<pk>[\d]+)/clinic/$', views.DoctorClinicView.as_view()),
    url(r'^(?P<pk>[\d]+)/patients/$', views.DoctorPatientListView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment/$', views.DoctorAppointmentView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment/history$', views.DoctorAppointmentHistoryView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment/visit$', views.DoctorAppointmentVisitView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment/(?P<appointment_id>[\d]+)/status/$', views.DoctorStatusView.as_view()),
    url(r'^(?P<pk>[\d]+)/clinic/(?P<clinic_id>[\d]+)/appointment_slots/$', views.DoctorAppointmentSlotView.as_view()),
    url(r'^(?P<pk>[\d]+)/visit/$', views.DoctorVisitView.as_view()),
    url(r'^(?P<pk>[\d]+)/review/$', views.DoctorReviewView.as_view()),
]
