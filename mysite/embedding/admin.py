from django.contrib import admin

# Register your models here.
from .models import UserProfile, TokenConsumption, PromptModel

admin.site.register(UserProfile)
admin.site.register(TokenConsumption)
admin.site.register(PromptModel)