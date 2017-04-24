from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users$', views.createUser),
    url(r'^login$', views.loginUser),
    url(r'^books$', views.indexBook),
    url(r'^logout$', views.logout),
    url(r'^books/new$', views.newBook),
    url(r'^reviews$', views.createBookAndReview),
    url(r'^books/(?P<id>\d+)$', views.showBook),
    url(r'^reviews/(?P<id>\d+)/delete$', views.deleteReview),
    url(r'^reviews/(?P<id>\d+)$', views.createReview),
    url(r'^users/(?P<id>\d+)$', views.showUser),
]