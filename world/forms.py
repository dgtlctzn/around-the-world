from django import forms

class SignIn(forms.Form):

    username = forms.CharField()
    password = forms.CharField()


class SignUp(forms.Form):

    username = forms.CharField()
    password = forms.CharField()
