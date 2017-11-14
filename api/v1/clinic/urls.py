from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[\d]+)$', views.ClinicView.as_view()),
    url(r'^(?P<pk>[\d]+)/test/$', views.TestView.as_view()),
    url(r'^(?P<pk>[\d]+)/review/$', views.ClinicReviewView.as_view()),
]
