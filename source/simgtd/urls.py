from django.conf.urls import patterns, include, url

from django.contrib import admin
from simgtd.login_views import logout, login

admin.autodiscover()

from simgtd import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simgtd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # for auth
    url(r'^login/', login),
    url(r'^logout/', logout),

    # for test app
    url(r'^polls/', include('polls.urls', namespace='polls')),

    # for simple gtd
    url(r'^about/', views.about),
    url(r'^gtd/', views.say),
    url(r'^goal/list/', views.goals),
    url(r'^goal/add/', views.add_goal),
    url(r'^goal/edit/(?P<gid>\d+)', views.edit_goal),
    url(r'^action/list/', views.action_list),
    url(r'^action/update/', views.action_update),
    url(r'^action/(?P<aid>\d+)', views.action_get),

    # for NLP
    #url(r'^nlp/', include('nlp.urls', namespace='nlp')),

    # for common
    url(r'^$', views.home),
    # url(r'^__main__/', views.main),
)
