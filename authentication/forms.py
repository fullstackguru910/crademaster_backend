from allauth.account.forms import LoginForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

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
