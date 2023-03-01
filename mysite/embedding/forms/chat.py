from django import forms

import embedding.static_values as sc


class ChatForm(forms.Form):
    password = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': "Need a secret word :D"}))
    message = forms.CharField(required=True, max_length=10000, widget=forms.Textarea(
                                 attrs={'class': 'message form-control', 'placeholder': "Limit 10,000 chars. "
                                                                                            "Required"}))
    character = forms.ChoiceField(required=True, choices=sc.CHAT_TYPES, widget=forms.Select(attrs={'class': 'character form-select', }))
    training_model = forms.ChoiceField(required=True, choices=sc.TRAINING_MODELS, widget=forms.Select(attrs={'class': 'character form-select', }))
