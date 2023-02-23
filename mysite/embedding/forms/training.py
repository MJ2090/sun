from django import forms

class TrainingForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(max_length=10000, widget=forms.Textarea(
                                 attrs={'class': 'form-control', 'placeholder': ('Limit 10,000 chars')}))