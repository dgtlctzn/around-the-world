from django import forms
# from .models import User
from django.contrib.auth import authenticate, get_user_model

class SignIn(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'username'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'password'
    }))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Username and password do not match')
            if not user.check_password(password):
                raise forms.ValidationError('Username and password do not match')
            return super(SignIn, self).clean()


User = get_user_model()


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