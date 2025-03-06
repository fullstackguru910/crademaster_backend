import secrets
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.forms import LoginForm, default_token_generator
from allauth.account.utils import (
    user_pk_to_url_str,
    user_username,
)
from allauth.socialaccount.models import EmailAddress

from dj_rest_auth.forms import AllAuthPasswordResetForm
from authentication.models import EmailVerificationCode

User = get_user_model()


class CustomLoginForm(LoginForm):

    def clean(self):
        cleaned_data = super().clean()
        login = self.cleaned_data["login"]

        if login:
            try:
                user = User.objects.get(email=login)
                if not user.is_superuser:
                    raise ValidationError("Login is restricted to administrator accounts only.")
            except User.DoesNotExist:
                pass        
        return cleaned_data


class CustomResetPasswordForm(AllAuthPasswordResetForm):

    def generate_verification_code(self):
        return ''.join(secrets.choice('0123456789') for _ in range(6))

    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)
            code = self.generate_verification_code()
            uid = user_pk_to_url_str(user)

            email_address = EmailAddress.objects.get(user=user)
            EmailVerificationCode.objects.update_or_create(
                email_address=email_address,
                defaults={
                    'code': code,
                    'uid': uid,
                    'token': temp_key 
                }
            )

            context = {
                'current_site': current_site,
                'user': user,
                'request': request,
                'token': temp_key,
                'uid': uid,
                'key': code
            }
            if (
                allauth_account_settings.AUTHENTICATION_METHOD != allauth_account_settings.AuthenticationMethod.EMAIL
            ):
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )
        return self.cleaned_data['email']
