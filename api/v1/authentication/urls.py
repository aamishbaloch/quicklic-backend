from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/', views.RegistrationView.as_view(), name='register'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^verify/', views.VerificationView.as_view(), name='verify'),
]
