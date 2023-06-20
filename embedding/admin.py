from django.contrib import admin

# Register your models here.
from .models import FruitOrder, TherapyAssessment, DepressionAssessment, VisitorDialogue, SuicideAssessment, EmbeddingDocument, VisitorProfile, TherapyProfile, OcrRecord, QuizRecord, UserProfile, TokenConsumption, PromptModel, EmbeddingModel, Contact, Dialogue

admin.site.register(Contact)
admin.site.register(Dialogue)
admin.site.register(EmbeddingModel)
admin.site.register(EmbeddingDocument)
admin.site.register(OcrRecord)
admin.site.register(PromptModel)
admin.site.register(QuizRecord)
admin.site.register(TherapyProfile)
admin.site.register(TokenConsumption)
admin.site.register(UserProfile)
admin.site.register(VisitorProfile)
admin.site.register(SuicideAssessment)
admin.site.register(VisitorDialogue)
admin.site.register(DepressionAssessment)
admin.site.register(TherapyAssessment)
admin.site.register(FruitOrder)
