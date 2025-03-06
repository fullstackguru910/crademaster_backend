from django.http import JsonResponse
from dj_rest_auth.registration.views import RegisterView

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView

from .models import EmailVerificationCode
from .serializers import CustomRegisterSerializer, EmailVerificationCodeSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class VerifyEmailCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        verification_code = request.data.get("verification_code")

        try:
            verification = EmailVerificationCode.objects.get(email_address__email=email, code=verification_code)
            
            if verification.is_expired:
                return JsonResponse({"error": "Verification code has expired"}, status=400)

            # You can now mark the email as verified in the EmailAddress model
            emailaddress = verification.email_address
            emailaddress.verified = True
            emailaddress.save()

            return JsonResponse({"success": "Email verified successfully!"}, status=200)

        except EmailVerificationCode.DoesNotExist:
            return JsonResponse({"error": "Invalid verification code"}, status=400)


class PasswordResetLookupView(RetrieveAPIView):
    queryset = EmailVerificationCode.objects.all()
    serializer_class = EmailVerificationCodeSerializer
    lookup_field = 'code'
    permission_classes = [AllowAny]
