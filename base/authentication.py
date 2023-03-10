# from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from user.models import User

class PhoneEmailAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        username = kwargs.get('email', None)
        try:
            if "@" in username:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
                return None
            else:
                user = User.objects.get(phone=username)
                if user.check_password(password):
                    return user
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None