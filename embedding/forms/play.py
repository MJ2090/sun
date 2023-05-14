from django import forms
import embedding.static_values as sc


class PlayForm(forms.Form):
    image_f = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control'}))
    llm_model = forms.ChoiceField(required=True, choices=sc.TRAINING_MODELS, widget=forms.Select(
        attrs={'class': 'character form-select', }))
