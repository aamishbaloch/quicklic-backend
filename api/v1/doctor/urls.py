from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[\d]+)$', views.DoctorView.as_view()),
    url(r'^$', views.DoctorListView.as_view()),
    url(r'^(?P<pk>[\d]+)/clinic/$', views.DoctorClinicView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment/$', views.DoctorAppointmentView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment/(?P<appointment_id>[\d]+)/status/$', views.DoctorStatusView.as_view()),
    url(r'^(?P<pk>[\d]+)/appointment_slots/$', views.DoctorAppointmentSlotView.as_view()),
]
