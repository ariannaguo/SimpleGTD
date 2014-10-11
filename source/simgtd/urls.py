from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from simgtd import views, settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simgtd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # for auth
    # url(r'^login/$', views.login),
    # url(r'^logout/$', views.logout),

    # for test app
    url(r'^polls/', include('polls.urls', namespace='polls')),

    # for simple gtd
    url(r'^$', views.say),
    # url(r'^__main__/', views.main),
    url(r'^say/', views.say),
)
