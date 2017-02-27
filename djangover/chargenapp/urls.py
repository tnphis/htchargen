import views

from django.conf.urls import url

urlpatterns = [
	url(r'^$', views.redir),
	url(r'^client/.*', views.index),
	url(r'^api', views.api),
	url(r'^auth', views.auth)
]
