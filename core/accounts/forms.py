from django import forms

class CustomLoginForm(forms.Form):
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)