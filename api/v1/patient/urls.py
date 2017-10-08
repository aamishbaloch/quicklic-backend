from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.PatientView.as_view()),
    url(r'^list', views.PatientListView.as_view()),
]
