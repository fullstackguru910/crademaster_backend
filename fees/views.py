from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from authentication.mixins import StaffRequiredMixin
from .models import Fee, RoyaltyFee

class FeeListView(StaffRequiredMixin, ListView):
    model = Fee
    template_name = 'fees/list.html'
    context_object_name = 'fees'


class FeeUpdateView(StaffRequiredMixin, UpdateView):
    model = Fee
    fields = ['min_investment', 'max_investment', 'hours', 'fee_percentage']
    template_name = 'fees/update.html'
    context_object_name = 'fee'
    success_url = reverse_lazy('fee_list')

    def get_object(self):
        return Fee.objects.get(id=self.kwargs['pk'])


class RoayltyFeeListView(StaffRequiredMixin, ListView):
    model = RoyaltyFee
    template_name = 'fees/royalty_list.html'
    context_object_name = 'fees'


class RoyaltyFeeUpdateView(StaffRequiredMixin, UpdateView):
    model = RoyaltyFee
    fields = ['min_investment', 'max_investment', 'fee_percentage']
    template_name = 'fees/royalty_update.html'
    context_object_name = 'fee'
    success_url = reverse_lazy('royalty_fee_list')

    def get_object(self):
        return RoyaltyFee.objects.get(id=self.kwargs['pk'])
