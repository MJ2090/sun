from django import forms


class SummaryForm(forms.Form):
    text = forms.CharField(required=True, max_length=10000, widget=forms.Textarea(
        attrs={'class': 'summary form-control', 'placeholder': "Limit 10,000 chars. "}))
    summary_text = forms.CharField(required=True, max_length=10000, widget=forms.Textarea(
        attrs={'disabled': 'true', 'class': 'summary form-control', 'placeholder': "... "}))
