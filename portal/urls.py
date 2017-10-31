from django.conf.urls import url

from portal import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^home$', views.PortalHomeView.as_view(), name='home'),
    url(r'^profile$', views.ProfileView.as_view(), name='profile'),
]