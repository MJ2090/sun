from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
                                 attrs={'class': 'form-control form-username', 'placeholder': "username"}))
    email = forms.EmailField(required=True, max_length=50, widget=forms.EmailInput(
                                 attrs={'class': 'form-control form-email', 'placeholder': "user@exapmle.com"}))
    password = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput(
                                 attrs={'class': 'form-control form-password'}))