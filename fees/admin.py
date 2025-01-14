from django.contrib import admin
from .models import Fee, RoyaltyFee


class FeeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'min_investment', 'max_investment', 'fee_percentage', 'hours']
    list_filter = ['fee_percentage']
    search_fields = ['min_investment', 'max_investment', 'fee_percentage']
    ordering = ['min_investment']
    fields = ['min_investment', 'max_investment', 'fee_percentage', 'hours']


admin.site.register(Fee, FeeAdmin)
admin.site.register(RoyaltyFee)
