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

    #url(r'^pastebin/', include('pastebin.urls', namespace='pastebin')),

    # for simple gtd
    #url(r'^gtd/', include('gtd.urls', namespace='gtd')),
    url(r'^say/', views.say),
    url(r'^about/', views.about),
    url(r'^gtd/', views.say),

    # for NLP
    #url(r'^nlp/', include('nlp.urls', namespace='nlp')),

    # for common
    url(r'^$', views.home),
    # url(r'^__main__/', views.main),
)
