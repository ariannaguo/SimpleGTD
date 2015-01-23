import datetime
from django.contrib import admin

from simgtd import settings as app_settings
from simgtd.models import Constants, Status, Priority, Goal, Action, ActionComment, Setting


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

    def queryset(self, request):
        qs = super(GoalAdmin, self).queryset(request)
        return qs.filter(created_by=request.user)


class ActionAdmin(admin.ModelAdmin):

    list_display = ('subject', 'hours', 'minutes', 'created_date', 'start_date', 'due_date', 'status')
    list_filter = ('status', 'created_date', 'due_date')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    search_fields = ('subject', 'memo')
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if obj.completed_date is None and obj.status.id == Constants.status_completed:
            obj.completed_date = datetime.datetime.now()
        obj.save()

    def queryset(self, request):
        qs = super(ActionAdmin, self).queryset(request)
        return qs.filter(created_by=request.user)


admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(ActionComment)
admin.site.register(Setting)


if app_settings.DEBUG:
    # do something funny
    pass