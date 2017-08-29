from django.conf.urls import url, include

from website import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contact_us$', views.ContactUsView.as_view(), name='contact_us')
]