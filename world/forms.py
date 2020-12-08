from django import forms
from .models import User

class SignIn(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'username'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'password'
    }))


class SignUp(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'username'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'password'
    }))

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    def clean_password(self):
        password = self.cleaned_data['password']
        if not 3 < len(password) < 11:
            raise forms.ValidationError('Please enter a password of at least 4 and no more than 10 characters')
        return password