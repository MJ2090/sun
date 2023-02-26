from django import forms


class SignupForm(forms.Form):
    password = forms.CharField(required=True, max_length=20, widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': "********"}))
    email = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': "user@exapmle.com"}))