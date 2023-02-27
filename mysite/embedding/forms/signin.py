from django import forms


class SigninForm(forms.Form):
    password = forms.CharField(required=True, max_length=20, widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': "********"}))
    username = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
                                 attrs={'class': 'form-control form-username', 'placeholder': "username"}))