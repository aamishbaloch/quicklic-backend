from django.conf.urls import url, include

from website import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contact_us$', views.ContactUsView.as_view(), name='contact-us'),
    url(r'^(?P<blog_id>\w+)/blog$', views.BlogView.as_view(), name='blog'),
    url(r'^blogs$', views.BlogListView.as_view(), name='blog-list'),
]