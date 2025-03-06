import secrets

from allauth.account.adapter import DefaultAccountAdapter

from .models import EmailVerificationCode

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        verification_code = self.generate_verification_code()
        EmailVerificationCode.objects.update_or_create(
            email_address=emailconfirmation.email_address,
            defaults={
                'code': verification_code,
            }
        )

        ctx = {
            "user": emailconfirmation.email_address.user,
            "key": verification_code,
        }
        
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)

    def generate_verification_code(self):
        """Generate a unique verification code"""
        return ''.join(secrets.choice('0123456789') for _ in range(6))
