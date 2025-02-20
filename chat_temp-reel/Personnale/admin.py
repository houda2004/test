from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(Ill)
admin.site.register(Symptom)
admin.site.register(EmailVerification)