from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.NotificationView.as_view()),
    url(r'^(?P<pk>[\d]+)/read$', views.NotificationUpdateView.as_view()),
]
