from django import forms
from embedding.models import PromptModel

import embedding.static_values as sc


class GagaForm(forms.Form):
    message = forms.CharField(required=True, max_length=10000, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Type your thoughts"}))
    character = forms.ChoiceField(required=True, choices=sc.GAGA_TYPES, widget=forms.Select(
        attrs={'class': 'character form-select', }))
    dialogue_id = forms.CharField(required=True, max_length=21, widget=forms.TextInput())
    source_id = forms.CharField(required=True, max_length=21, widget=forms.TextInput(), initial='openai')

