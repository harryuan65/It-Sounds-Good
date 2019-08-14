from django import forms

class UrlForm(forms.Form):
    url = forms.CharField(label='',widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'example: https://www.youtube.com/watch?v=D6esTdOLXh4'}))
    