from django import forms
import embedding.static_values as sc


class ImageForm(forms.Form):
    text = forms.CharField(required=True, max_length=1000, widget=forms.Textarea(
        attrs={'class': 'image-generation form-control', 'placeholder': "Limit 1,000 chars. "
               "Required"}))
    style = forms.ChoiceField(required=True, choices=sc.IMAGE_TYPES, widget=forms.Select(
        attrs={'class': 'image-typle form-select', }))
