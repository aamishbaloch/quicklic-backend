from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^featured/$', views.TestView.as_view()),

]
