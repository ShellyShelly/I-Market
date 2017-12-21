from .models import User


class UserAuth(object):
    def authenticate(self, request=None, username=None, password=None):
        if request is not None:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password) and user.is_active:
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, request):
        try:
            user = User.objects.get(pk=request)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
