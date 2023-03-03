from django import forms


class TranslationForm(forms.Form):
    text = forms.CharField(required=True, max_length=10000, widget=forms.Textarea(
                                 attrs={'class': 'translation form-control', 'placeholder': "Limit 10,000 chars. "
                                                                                            "Required"}))