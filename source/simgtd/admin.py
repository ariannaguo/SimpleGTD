import datetime
from django.contrib import admin

from simgtd import settings as app_settings
from simgtd.models import Constants, Status, Priority, Goal, Action


class GoalAdmin(admin.ModelAdmin):

    list_display = ('subject', 'start_date', 'due_date', 'progress',
                    'status', 'priority')
    list_filter = ('status', 'start_date', 'due_date')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    search_fields = ('subject', 'memo')
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if obj.completed_date is None and obj.status.id == Constants.status_completed:
            obj.completed_date = datetime.datetime.now()
        obj.save()


admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Action)


if app_settings.DEBUG:
    # do something funny
    pass