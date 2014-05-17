from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'home.views.login', name='login'),
    url(r'^home$', 'home.views.home', name='home'),
    url(r'^spotify', 'home.views.spotify', name='spotify'),
    url(r'^beats', 'home.views.beats', name='beats'),
    url(r'^logout$', 'home.views.logout', name='logout'),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
