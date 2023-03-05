from django import forms


class PromptModelForm(forms.Form):
    name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "new model name"}))
    history = forms.CharField(required=True, max_length=1000, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': "Limit 1,000 chars. "}))
