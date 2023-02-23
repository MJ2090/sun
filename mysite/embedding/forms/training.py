from django import forms


class TrainingForm(forms.Form):
    q1 = forms.CharField(required=True, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question', 'placeholder': "Limit 200 chars, required"}))
    q2 = forms.CharField(required=False, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question', 'placeholder': "Limit 200 chars"}))
    q3 = forms.CharField(required=False, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question', 'placeholder': "Limit 200 chars"}))
    q4 = forms.CharField(required=False, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question', 'placeholder': "Limit 200 chars"}))
    q5 = forms.CharField(required=False, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question', 'placeholder': "Limit 200 chars"}))
    message = forms.CharField(max_length=10000, widget=forms.Textarea(
                                 attrs={'class': 'form-control', 'placeholder': "Limit 10,000 chars"}))