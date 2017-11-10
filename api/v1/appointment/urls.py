from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AppointmentView.as_view()),
    url(r'^(?P<pk>[\d]+)/visit/$', views.AppointmentVisitView.as_view()),
    url(r'^(?P<appointment_id>[\d]+)/visit/(?P<pk>[\d]+)$', views.AppointmentVisitUpdateView.as_view()),
]
