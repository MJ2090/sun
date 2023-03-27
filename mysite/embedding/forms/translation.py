from django import forms

import embedding.static_values as sc

class TranslationForm(forms.Form):
    text = forms.CharField(required=True, max_length=10000, widget=forms.Textarea(
        attrs={'class': 'translation form-control', 'placeholder': "Limit 10,000 chars. "}))
    translated_text = forms.CharField(required=True, max_length=4000, widget=forms.Textarea(
        attrs={'disabled': 'true', 'class': 'translation form-control', 'placeholder': "... "}))
    target = forms.ChoiceField(required=True, choices=sc.TRANSLATION_TYPES, widget=forms.Select(
        attrs={'class': 'image-typle form-select', }))
