from django import forms
from .models import User

class SignIn(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'username'
    }))
    password = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'password'
    }))
    # class Meta:
    #     model = User
    #     fields = [
    #         'username',
    #         'password'
    #     ]


class SignUp(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'username'
    }))
    password = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'password'
    }))

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if not 5 < len(username) < 16:
            raise forms.ValidationError('Please enter a username of at least 6 and no more than 15 characters')
        return username