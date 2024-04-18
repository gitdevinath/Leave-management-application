from django.contrib import admin
from . models import addemployee, addLeave, profile

# Register your models here.
admin.site.register(addemployee)
admin.site.register(addLeave)
admin.site.register(profile)
