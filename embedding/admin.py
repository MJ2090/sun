from django.contrib import admin

# Register your models here.
from .models import TherapyProfile, OcrRecord, QuizRecord, UserProfile, TokenConsumption, PromptModel, EmbeddingModel, Contact, Dialogue

admin.site.register(UserProfile)
admin.site.register(TokenConsumption)
admin.site.register(PromptModel)
admin.site.register(EmbeddingModel)
admin.site.register(Contact)
admin.site.register(Dialogue)
admin.site.register(OcrRecord)
admin.site.register(QuizRecord)
admin.site.register(TherapyProfile)
