from django.conf.urls import patterns, include, url
from chargenapp import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'htchargen.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^$', views.redir),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^app/', include('chargenapp.urls'))
)
