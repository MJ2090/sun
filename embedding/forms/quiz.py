from django import forms
import embedding.static_values as sc


class QuizForm(forms.Form):
    image_f = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control hidden'}))
    llm_model = forms.ChoiceField(required=True, choices=sc.QUIZ_MODELS, widget=forms.RadioSelect(attrs={'class': 'mt-1'}))
