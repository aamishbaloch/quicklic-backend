from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.PatientView.as_view()),
    url(r'^list/', views.PatientListView.as_view()),
    url(r'^clinic/$', views.PatientClinicView.as_view()),
    url(r'^clinic/(?P<clinic_id>[\d]+)', views.PatientClinicView.as_view()),
]
