from django.urls import path, re_path, include
from django.views.generic import TemplateView

from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
)

from dj_rest_auth.views import (
    PasswordResetConfirmView,
)

from authentication.views import (
    CustomRegisterView,
    VerifyEmailCodeView,
    password_reset_confirm_redirect
)


urlpatterns = [
    path('', include('dj_rest_auth.urls')),

    path('register/', CustomRegisterView.as_view(), name="rest_register"),
    path('register/verify-email/', VerifyEmailCodeView.as_view(), name='verify_email_code'),
    path('register/resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),

    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email',
    ),
    path(
        'account-email-verification-sent/', TemplateView.as_view(),
        name='account_email_verification_sent',
    ),

    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
]
