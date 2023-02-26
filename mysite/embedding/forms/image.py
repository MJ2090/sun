from django import forms


class ImageForm(forms.Form):
    password = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': "Need a secret word :D"}))
    text = forms.CharField(required=True, max_length=1000, widget=forms.Textarea(
                                 attrs={'class': 'grammar form-control', 'placeholder': "Limit 1,000 chars. "
                                                                                            "Required"}))