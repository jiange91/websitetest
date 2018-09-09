from django import forms
from accounts.models import User
import hashlib
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


def hash_code(s, salt='confirm'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


class LoginForm(forms.Form):
    email = forms.CharField(label="", max_length=128,required=True,
                               widget=forms.EmailInput(attrs={'id':'email', 'class': 'form-control input-medium','placeholder':'Email'}))
    password = forms.CharField(label="", max_length=256,
                               widget=forms.PasswordInput(attrs={'id':'password', 'class': 'form-control input-medium','placeholder':'Password'}))

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password = hash_code(password)
        try:
            user = User.objects.get(email=email)
            if not user.has_confirmed:
                message = 'Your account is not activated yet, please check your email and find the link'
                self.cleaned_data['message'] = message
                return self.cleaned_data
            if not user.password == password:
                message = 'Wrong password'
                self.cleaned_data['message'] = message
                return self.cleaned_data
            else:
                self.cleaned_data['user'] = user
                message = 'Login successful'
                self.cleaned_data['message'] = message
                return self.cleaned_data
        except ObjectDoesNotExist:
            message = 'Invalid account'
            self.cleaned_data['message'] = message
            return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label='', max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}
    ))
    password1 = forms.CharField(label='', max_length=256, widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'password'}
    ))
    password2 = forms.CharField(label='', max_length=256, widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'password confirmation'}
    ))
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'class':'form-control', 'placeholder':'Email'}
    ))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'email'}
        labels = {'username':'username', 'email':'email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'})}


class PswForm(forms.Form):
    password1 = forms.CharField(label='New Password', max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    password2 = forms.CharField(label='Confirmation password', max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))