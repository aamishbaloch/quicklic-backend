from django.conf.urls import url

from portal import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^home$', views.PortalHomeView.as_view(), name='home'),
    url(r'^profile$', views.ProfileView.as_view(), name='profile'),
    url(r'^doctor_setting$', views.DoctorSettingView.as_view(), name='doctor_setting'),
    url(r'^doctor/(?P<pk>[\d]+)/key_factors$', views.DoctorKeyFactorsView.as_view(), name='doctor_key_factors'),
    url(r'^doctor/operations$', views.DoctorOperationsView.as_view(), name='doctor_operations'),
    url(r'^patients$', views.PatientsView.as_view(), name='patients'),
]