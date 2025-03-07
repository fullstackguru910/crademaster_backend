from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth import get_user_model

from authentication.mixins import StaffRequiredMixin
from .models import Event

User = get_user_model()


class EventListView(StaffRequiredMixin, ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'


class UserEventListView(StaffRequiredMixin, ListView):
    model = Event
    template_name = 'events/user/list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(users__pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_pk)
        context['user'] = user
        return context


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


class RemoveUserFromEventView(View):
    def post(self, request, event_id, user_id):
        event = get_object_or_404(Event, pk=event_id)
        user = get_object_or_404(User, id=user_id)

        if user not in event.users.all():
            return HttpResponseForbidden("User is not part of the event")

        event.users.remove(user)

        return redirect('user_list')
