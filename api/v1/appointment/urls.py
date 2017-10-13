# {
# 	"doctor": "1",
# 	"clinic": "1",
# 	"start_datetime": "2017-10-13 01:00:00",
# 	"end_datetime": "2017-10-13 01:30:00",
# 	"duration": "20",
# 	"reason": "1"
# }

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add$', views.AppointmentCreateView().as_view()),
    # url(r'^list', views.DoctorListView.as_view(), name='doctor-list'),
]
