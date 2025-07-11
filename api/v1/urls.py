from django.conf.urls import url, include
from api.v1.authentication import urls as auth_urls
from api.v1.doctor import urls as doctor_urls
from api.v1.patient import urls as patient_urls
from api.v1.appointment import urls as appointment_urls
from api.v1.clinic import urls as clinic_urls
from api.v1.test import urls as test_urls
from api.v1.review import urls as review_urls
from api.v1.notification import urls as notification_urls
from . import views

urlpatterns = [
    url(r'^country/', views.CountryView.as_view()),
    url(r'^city/', views.CityView.as_view()),
    url(r'^specialization/', views.SpecializationView.as_view()),
    url(r'^service/', views.ServiceView.as_view()),
    url(r'^occupation/', views.OccupationView.as_view()),
    url(r'^reason/', views.AppointmentReasonView.as_view()),
    url(r'^auth/', include(auth_urls)),
    url(r'^doctor/', include(doctor_urls)),
    url(r'^patient/', include(patient_urls)),
    url(r'^appointment/', include(appointment_urls)),
    url(r'^clinic/', include(clinic_urls)),
    url(r'^test/', include(test_urls)),
    url(r'^review/', include(review_urls)),
    url(r'^notification/', include(notification_urls)),
]