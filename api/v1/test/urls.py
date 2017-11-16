from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lab/$', views.TestLabView.as_view()),
    url(r'^featured/$', views.TestView.as_view()),
    url(r'^(?P<pk>[\d]+)$', views.TestDetailView.as_view()),

]
