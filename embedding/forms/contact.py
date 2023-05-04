from django import forms


class ContactForm(forms.Form):        
    username = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username"}))
    email = forms.EmailField(required=True, max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "you@example.com"}))
    message = forms.CharField(required=True, max_length=1500, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Contents"}))