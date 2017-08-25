from django.conf.urls import url, include

from website.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home')
]