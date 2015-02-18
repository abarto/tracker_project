from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

from socketio import sdjango
sdjango.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'tracker_project.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('home')},
        name='logout'
    ),
    url(r'^tracker/', include('tracker.urls', 'tracker')),
    url(r'^socket\.io', include(sdjango.urls))
)
