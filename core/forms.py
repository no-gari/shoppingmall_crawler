from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(label='아이디', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    field_order = ['username', 'password', 'email']

    class Meta:
        model = User
        fields = {
            'email', 'username', 'password'
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='아이디', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    field_order = ['username', 'password']

    class Meta:
        model = User
        fields = {
            'username', 'password'
        }
