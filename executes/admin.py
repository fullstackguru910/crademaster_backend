from django.contrib import admin

from .models import Execute

class ExecuteAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'duration', 'profit_percent', 'created']
    list_filter = ['user', 'duration']
    search_fields = ['user__username', 'amount']
    fields = ['user', 'amount', 'duration', 'profit_percent', 'created']


admin.site.register(Execute, ExecuteAdmin)
