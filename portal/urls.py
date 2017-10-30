from django.conf.urls import url, include

from portal import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name='login'),
]