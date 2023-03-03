from django import forms

import embedding.static_values as sc


class ChatForm(forms.Form):
    message = forms.CharField(required=True, max_length=10000, widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': "Type your thoughts"}))
    character = forms.ChoiceField(required=True, choices=sc.CHAT_TYPES, widget=forms.Select(attrs={'class': 'character form-select', }))
    training_model = forms.ChoiceField(required=True, choices=sc.TRAINING_MODELS, widget=forms.Select(attrs={'class': 'character form-select', }))
