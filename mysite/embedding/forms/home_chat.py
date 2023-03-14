from django import forms

import embedding.static_values as sc


class HomeChatForm(forms.Form):
    message = forms.CharField(required=True, max_length=10000, widget=forms.TextInput(
        attrs={'class': 'home-chat-message', 'placeholder': "Type your thoughts"}))
    enable_speech = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', }))
