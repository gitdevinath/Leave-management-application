from django.contrib.auth.backends import BaseBackend
from .models import addemployee

class AddEmployeeBackend(BaseBackend):
    def autheticate(self, request, username=None, password=None):
        try:
            user = addemployee.objects.get(username=username)
            if user.check_password(password):
                return user
        except addemployee.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return addemployee.objects.get(pk=user_id)
        except addemployee.DoesNotExist:
            return None
