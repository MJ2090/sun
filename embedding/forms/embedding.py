from django import forms
from embedding.models import EmbeddingModel
import embedding.static_values as sc


class TrainingForm(forms.Form):
    name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
        attrs={'class': 'embedding-name form-control', 'placeholder': "Limit 100 chars"}))
    text = forms.CharField(max_length=200000, widget=forms.Textarea(
        attrs={'class': 'training-text form-control', 'placeholder': "Limit 200,000 chars"}))
    reject_message = forms.CharField(required=True, max_length=500, widget=forms.TextInput(
        attrs={'class': 'embedding-name form-control', 'placeholder': "Limit 500 chars", 'value': 'Answer Not Found.'}))
    file_f = forms.FileField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control'}))


class QuestionForm(forms.Form):
    llm = forms.ChoiceField(required=True, choices=sc.QUESTION_LLM_TYPES, widget=forms.Select(
        attrs={'class': 'character form-select', }))
    character = forms.ChoiceField(required=True, choices=(), widget=forms.Select(
        attrs={'class': 'character form-select', }))
    question = forms.CharField(required=True, max_length=500, widget=forms.Textarea(
        attrs={'class': 'embedding-question form-control', 'placeholder': "Limit 500 chars"}))
    answer = forms.CharField(required=True, max_length=2000, widget=forms.Textarea(
        attrs={'disabled': 'true', 'class': 'embedding-answer form-control', 'placeholder': "..."}))
    enable_speech = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', }))
