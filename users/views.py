from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin
from authentication.serializers import CustomUserSerializer

from .models import CustomUser
from .serializers import UploadedFilesSerializer

from transactions.handler import TronTransaction

tron = TronTransaction()


class UserListView(StaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/list.html'
    context_object_name = 'users'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_staff=True)
        sort_by = self.request.GET.get('sort_by', 'tron_balance')
        
        # Get the balances for each user and sort based on them
        if sort_by == 'TRX':
            queryset = sorted(queryset, key=lambda user: tron.get_tron_balance(user.cm_wallet), reverse=True)
        elif sort_by == 'USDT':
            queryset = sorted(queryset, key=lambda user: tron.get_usdt_balance(user.cm_wallet), reverse=True)
        return queryset


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
