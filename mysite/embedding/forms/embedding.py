from django import forms
from embedding.models import EmbeddingModel


class TrainingForm(forms.Form):
    name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
        attrs={'class': 'embedding-name form-control', 'placeholder': "Limit 100 chars"}))
    text = forms.CharField(max_length=100000, widget=forms.Textarea(
        attrs={'class': 'training-text form-control', 'placeholder': "Limit 100,000 chars"}))


class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['character'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'character form-select', }),
            choices=[(o.uuid, o.name) for o in EmbeddingModel.objects.all()]
        )
    character = forms.ChoiceField(required=True, choices=(), widget=forms.Select(
        attrs={'class': 'character form-select', }))
    question = forms.CharField(required=True, max_length=200, widget=forms.Textarea(
        attrs={'class': 'embedding-question form-control', 'placeholder': "Limit 200 chars"}))
    answer = forms.CharField(required=True, max_length=2000, widget=forms.Textarea(
        attrs={'disabled': 'true', 'class': 'embedding-question form-control', 'placeholder': "..."}))