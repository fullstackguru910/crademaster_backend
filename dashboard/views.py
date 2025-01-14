import json
import calendar

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from fees.models import Fee

User = get_user_model()


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fees'] = Fee.objects.all()
        context['users'] = User.objects.filter(emailaddress__verified=True).distinct()
        monthly_users = (
            User.objects.annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(user_count=Count('id'))
            .order_by('month')
        )

        months = [calendar.month_abbr[entry['month'].month] for entry in monthly_users]
        user_counts = [entry['user_count'] for entry in monthly_users]

        context['months'] = json.dumps(months)
        context['user_counts'] = json.dumps(user_counts)
        return context
