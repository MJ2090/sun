from django import forms


class SigninForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
                                 attrs={'class': 'form-control form-username', 'placeholder': "username"}))
    password = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
                                 attrs={'class': 'form-control form-password', 'placeholder': "********"}))