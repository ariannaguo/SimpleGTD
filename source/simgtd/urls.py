from django.conf.urls import patterns, include, url

from django.contrib import admin
from simgtd.login_views import logout, login
from simgtd.user_views import profile, sms

admin.autodiscover()

from simgtd import views, mobile_views, internal_views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simgtd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # for auth
    url(r'^login/', login),
    url(r'^logout/', logout),

    # for user
    url(r'^me', profile),
    url(r'^mine/sms/', sms),

    # for test app
    url(r'^polls/', include('polls.urls', namespace='polls')),

    # for simple gtd
    url(r'^about/', views.about),
    url(r'^try/', views.djtry),
    url(r'^email/', views.email),
    url(r'^temp/', internal_views.use_template),

    url(r'^goal/list/', views.goals),
    url(r'^goal/add/', views.add_goal),
    url(r'^goal/edit/(?P<gid>\d+)', views.edit_goal),
    url(r'^goal/status/(?P<gid>\d+)', views.goal_status),
    url(r'^goal/overdue/', views.overdue, name='overdue_goals'),

    url(r'^action/list/', views.action_list),
    url(r'^action/update/', views.action_update),
    url(r'^action/(?P<aid>\d+)/$', views.action_get),
    url(r'^action/tags/$', views.action_tags),
    url(r'^action/tag/(?P<tag>[^/]+)/$', views.actions_of_tag),
    url(r'^action/(?P<aid>\d+)/comments/$', views.action_comments),
    url(r'^action/(?P<aid>\d+)/new_comment$', views.add_action_comment),
    url(r'^action/status/(?P<aid>\d+)', views.action_status),
    url(r'^action/overdue/', views.overdue, name='overdue_actions'),

    url(r'^sms/', mobile_views.send_sms),

    # for NLP
    #url(r'^nlp/', include('nlp.urls', namespace='nlp')),

    # for common
    url(r'^$', views.action_list, name='site_root'),
    # url(r'^__main__/', views.main),
)
