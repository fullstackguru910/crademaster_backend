from django.urls import path, re_path, include
from django.views.generic import TemplateView

from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
)

from authentication.views import (
    CustomRegisterView,
    VerifyEmailCodeView
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

    # path('register/', include('dj_rest_auth.registration.urls')),

    # path("login/", LoginView.as_view(), name="rest_login"),
    # path("logout/", LogoutView.as_view(), name="rest_logout"),
    # path("user/", UserDetailsView.as_view(), name="rest_user_details"),

    # path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    # path(
    #     "password/reset/confirm/<str:uidb64>/<str:token>/",
    #     password_reset_confirm_redirect,
    #     name="password_reset_confirm",
    # ),
    # path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
