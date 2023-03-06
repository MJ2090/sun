from django import forms


class ImageForm(forms.Form):
    text = forms.CharField(required=True, max_length=1000, widget=forms.Textarea(
                                 attrs={'class': 'image-generation form-control', 'placeholder': "Limit 1,000 chars. "
                                                                                            "Required"}))