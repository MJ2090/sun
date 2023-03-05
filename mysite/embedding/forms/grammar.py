from django import forms


class GrammarForm(forms.Form):
    text = forms.CharField(required=True, max_length=10000, widget=forms.Textarea(
        attrs={'class': 'grammar form-control', 'placeholder': "Limit 10,000 chars. "
               "Required"}))
