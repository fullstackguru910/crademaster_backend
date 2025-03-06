import asyncio
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin
from authentication.serializers import CustomUserSerializer

from .models import CustomUser
from .serializers import UploadedFilesSerializer


class UserListView(StaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/list.html'
    context_object_name = 'users'
    # paginate_by = 5

    async def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_staff=True)

        users = list(queryset)
        tasks = []

        for user in users:
            tasks.append(asyncio.create_task(self.fetch_balances(user)))

        await asyncio.gather(*tasks)
        print(users)
        return users

    async def fetch_balances(self, user):
        user.get_tron_balance
        user.get_usdt_balance


class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['profit_percent']
    template_name = 'users/update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_list')

    def get_object(self):
        return CustomUser.objects.get(id=self.kwargs['pk'])


# API view

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class IDFileUploadView(generics.CreateAPIView):
    serializer_class = UploadedFilesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
