from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer

from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.socialaccount.models import EmailAddress

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.serializers import ReferredUserSerializer
from executes.serializers import ExecuteHistorySerializer
from events.serializers import EventSerializer

from executes.models import Execute
from events.models import Event
from authentication.models import EmailVerificationCode

from authentication.forms import CustomResetPasswordForm
from transactions.handler import TronTransaction

tron = TronTransaction()
User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    referral = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )
    cm_wallet = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )
    cm_private_key = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )
    cm_public_key = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )
    cm_hex_address = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )

    event = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )

    def get_cleaned_data(self):
        """
        Extend cleaned data to include referral & event.
        """
        cleaned_data = super().get_cleaned_data()
        cleaned_data['referral'] = self.validated_data.get('referral', '')
        cleaned_data['event'] = self.validated_data.get('event', '')
        return cleaned_data

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if EmailAddress.objects.is_verified(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
            
            existing_email = EmailAddress.objects.filter(email=email).first()
            if existing_email and not existing_email.verified:
                existing_email.send_confirmation(self.context.get('request'))
                self.context['resend'] = existing_email.user

            #     raise serializers.ValidationError(
            #         _('This e-mail address is already registered but not verified. '
            #             'A new verification email has been sent to your inbox.')
            #     )
        return email
    
    def custom_signup(self, request, user):
        """
        Custom logic for referral code handling.
        """
        # admin = User.objects.get(is_staff=True)
        tron_account = tron.generate_address()
        user.cm_wallet = tron_account.get('base58check_address')
        user.cm_private_key = tron_account.get('private_key')
        user.cm_public_key = tron_account.get('public_key')
        user.cm_hex_address = tron_account.get('hex_address')

        referral_code = self.cleaned_data.get('referral')
        if referral_code:
            referred_by = User.objects.filter(referral_code=referral_code).first()
            if referred_by:
                user.referred_by = referred_by

        event_code = self.cleaned_data.get('event')
        if event_code:
            event = Event.objects.filter(code=event_code).first()
            if event:
                event.users.add(user)
        #         tron.transfer_usdt(admin.cm_wallet, admin.cm_private_key, user.cm_wallet, int(event.amount))

        # tron.transfer_tron(admin.cm_wallet, admin.cm_private_key, user.cm_wallet, 0.01)
        user.save()

    def save(self, request):
        if self.context.get('resend'):
            return self.context.get('resend')
        return super().save(request)


class CustomUserSerializer(serializers.ModelSerializer):
    usdt_balance = serializers.SerializerMethodField()
    tron_balance = serializers.SerializerMethodField()
    total_balance = serializers.SerializerMethodField()
    total_profits = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    total_deposits = serializers.SerializerMethodField()
    total_execute = serializers.SerializerMethodField()
    elapsed = serializers.SerializerMethodField()
    referred_users = serializers.SerializerMethodField()
    executes = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'cm_wallet',
            'referral_code',
            'profit_percent',
            'availability',
            'total_execute',
            'elapsed',
            'referred_users',
            'total_deposits',
            'usdt_balance',
            'tron_balance',
            'total_balance',
            'total_profits',
            'executes',
            'events',
        ]

    def get_total_balance(self, obj):
        return obj.get_balance
    
    def get_total_profits(self, obj):
        return obj.get_profits

    def get_tron_balance(self, obj):
        return obj.get_tron_balance
    
    def get_usdt_balance(self, obj):
        return obj.get_usdt_balance
    
    def get_total_deposits(self, obj):
        return obj.get_deposit_balance
    
    def get_availability(self, obj):
        return obj.availability

    def get_total_execute(self, obj):
        return obj.calculate_total_execute()
    
    def get_elapsed(self, obj):
        return obj.calculate_elapsed()
    
    def get_referred_users(self, obj):
        referred_users = User.objects.filter(referred_by=obj)
        return ReferredUserSerializer(referred_users, many=True).data
    
    def get_executes(self, obj):
        executes = Execute.objects.filter(user=obj)
        return ExecuteHistorySerializer(executes, many=True).data
    
    def get_events(self, obj):
        events = obj.events.all()
        return EventSerializer(events, many=True).data


class CustomPasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = CustomResetPasswordForm


class EmailVerificationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailVerificationCode
        fields = ['uid', 'token']
        read_only_fields = ['uid', 'token']

    def to_representation(self, instance):
        if instance.is_expired:
            raise ValidationError({"detail": "The verification code has expired."})
        return super().to_representation(instance)
