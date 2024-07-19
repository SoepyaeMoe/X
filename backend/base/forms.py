from django import forms
from .models import User
from django.contrib.auth.hashers import make_password

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8, max_length=20)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User does not exist")
        return email

class UserSignupForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, min_length=8, max_length=20)
    password2 = forms.CharField(required=True, min_length=8, max_length=20)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords doesn't match")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    def save(self):
        data = self.cleaned_data
        user = User.objects.create(
            name=data['name'],
            email=data['email'],
            password=make_password(data['password1'])
        )
        user.save()
        return user
    
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(required=True, min_length=8, max_length=20)
    new_password = forms.CharField(required=True, min_length=8, max_length=20)
    confirm_password = forms.CharField(required=True, min_length=8, max_length=20)

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Confirm passwords doesn't match")
        return confirm_password
    