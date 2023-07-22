from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.safestring import mark_safe
from .models import CustomUser

from Users.models import Profile

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    last_name=forms.CharField()
    first_name=forms.CharField()
    terms_conditions=forms.BooleanField(label=mark_safe('I have read and agree with the <a href="/terms_conditions" target="_blank">Terms and conditions</a> & <a href="/privacy_policy" target="_blank">Privacy Policy</a>'))

    class Meta:
        model = User
        fields= ['first_name','last_name','username','email', 'password1','password2','terms_conditions']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields= ['username','email']

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model=Profile
        fields=['image']


class CustomUserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    last_name=forms.CharField()
    first_name=forms.CharField()
    terms_conditions=forms.BooleanField(label=mark_safe('I have read and agree with the <a href="/terms_conditions" target="_blank">Terms and condititons</a> & <a href="/privacy_policy" target="_blank">Privacy Policy</a>'))

    class Meta:
        model = CustomUser
        fields= ['first_name','last_name','username','email', 'password1','password2','terms_conditions']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields= ['first_name','last_name','username','email',]

class UsersGroupForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all())
    users = forms.ModelChoiceField(
        queryset=CustomUser.objects.all())
