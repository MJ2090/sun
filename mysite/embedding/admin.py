from django.contrib import admin

# Register your models here.
from .models import UserProfile, TokenConsumption

admin.site.register(UserProfile)
admin.site.register(TokenConsumption)