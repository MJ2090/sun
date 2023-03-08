from django import forms
from embedding.models import PromptModel

import embedding.static_values as sc


class ChatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ChatForm, self).__init__(*args, **kwargs)
        self.fields['character'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'character form-select', }),
            choices=[(o.name, o.name) for o in PromptModel.objects.all()]
        )

    message = forms.CharField(required=True, max_length=10000, widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': "Type your thoughts"}))
    character = forms.ChoiceField(required=True, choices=sc.CHAT_TYPES, widget=forms.Select(attrs={'class': 'character form-select', }))
    training_model = forms.ChoiceField(required=True, choices=sc.TRAINING_MODELS, widget=forms.Select(attrs={'class': 'character form-select', }))
    enable_speech = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input', }))