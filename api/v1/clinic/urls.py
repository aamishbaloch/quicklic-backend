from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AppointmentView.as_view()),
    url(r'^list$', views.AppointmentListView.as_view()),
]
