from django import forms
import embedding.static_values as sc


class ImageForm(forms.Form):
    text = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(
        attrs={'class': 'image-generation form-control', 'placeholder': "Describe your imagination"}))
    style = forms.ChoiceField(required=True, choices=sc.IMAGE_TYPES, widget=forms.Select(
        attrs={'class': 'image-typle form-select', }))
    count = forms.ChoiceField(required=True, choices=sc.IMAGE_COUNTS, widget=forms.Select(
        attrs={'class': 'image-typle form-select', }))
