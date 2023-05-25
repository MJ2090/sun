from django import forms


class DemoForm(forms.Form):
    text = forms.CharField(required=True, max_length=10000, widget=forms.Textarea(
        attrs={'class': 'summary form-control', 'placeholder': "Limit 10,000 chars. "}))
    prompt = forms.CharField(required=True, max_length=1000, initial="总结下文", widget=forms.Textarea(
        attrs={'class': 'prompt form-control', 'placeholder': "Limit 10,00 chars. "}))
    result_text = forms.CharField(required=True, max_length=10000, widget=forms.Textarea(
        attrs={'disabled': 'true', 'class': 'summary form-control', 'placeholder': "... "}))
    temperature = forms.FloatField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'value': "0.9"}))
    character = forms.ChoiceField(required=True, choices=(), widget=forms.Select(
        attrs={'class': 'character form-select', }))
    question = forms.CharField(required=True, max_length=500, widget=forms.Textarea(
        attrs={'class': 'embedding-question form-control', 'placeholder': "Limit 500 chars"}))
