from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/', views.RegistrationView.as_view(), name='register'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^verify/', views.VerificationView.as_view(), name='verify'),
    url(r'^forgot_password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^password/verify/', views.ChangePasswordVerificationView.as_view(), name='change_password_verify'),
    url(r'^password/change/', views.ChangePasswordView.as_view(), name='change_password_change'),
]
