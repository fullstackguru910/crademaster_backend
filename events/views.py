from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from authentication.mixins import StaffRequiredMixin
from .models import Event

class EventListView(StaffRequiredMixin, ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'


class EventCreateView(StaffRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'amount']
    template_name = 'events/form.html'
    success_url = reverse_lazy('event_list')


class EventUpdateView(StaffRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'amount']
    template_name = 'events/update.html'
    context_object_name = 'event'
    success_url = reverse_lazy('event_list')

    def get_object(self):
        return Event.objects.get(id=self.kwargs['pk'])
