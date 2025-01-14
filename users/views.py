from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin
from authentication.serializers import CustomUserSerializer

from .models import CustomUser, IDFile
from .serializers import UploadedFilesSerializer


class UserListView(StaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(is_staff=True)


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
