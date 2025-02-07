from django.contrib import admin

from .models import EmailVerificationCode

@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'code', 'created', 'updated')
    search_fields = ('email_address__email', 'code')
    list_filter = ('created',)