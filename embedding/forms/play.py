from django import forms


class PlayForm(forms.Form):
    image = forms.CharField(required=True, max_length=1000000, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Image"}))
    image_f = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control'}))
