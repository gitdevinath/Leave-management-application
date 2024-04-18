from django.contrib.auth.models import User

def is_superuser(request):
    if request.user.is_authenticated:
        return {'is_superuser': request.user.is_superuser}
    return {'is_superuser': False}
