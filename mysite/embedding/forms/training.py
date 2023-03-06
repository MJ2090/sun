from django import forms


class TrainingForm(forms.Form):
    q1 = forms.CharField(required=True, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question form-control', 'placeholder': "Limit 200 chars. Required"}))
    q2 = forms.CharField(required=False, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question form-control', 'placeholder': "Limit 200 chars"}))
    q3 = forms.CharField(required=False, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question form-control', 'placeholder': "Limit 200 chars"}))
    q4 = forms.CharField(required=False, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question form-control', 'placeholder': "Limit 200 chars"}))
    q5 = forms.CharField(required=False, max_length=200, widget=forms.Textarea(
                                 attrs={'class': 'question form-control', 'placeholder': "Limit 200 chars"}))
    message = forms.CharField(max_length=100000, widget=forms.Textarea(
                                 attrs={'class': 'training-text form-control', 'placeholder': "Limit 100,000 chars"}))