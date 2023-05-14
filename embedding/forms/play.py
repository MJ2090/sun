from django import forms
import embedding.static_values as sc


class PlayForm(forms.Form):
    image = forms.CharField(required=True, max_length=1000000, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Image"}))
    image_f = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control'}))
    llm_model = forms.ChoiceField(required=True, choices=sc.TRAINING_MODELS, widget=forms.Select(
        attrs={'class': 'character form-select', }))
