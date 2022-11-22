from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
User = get_user_model()
from email_validate import validate, validate_or_fail


class Userloginform(forms.Form):
    username = forms.CharField(max_length=50, label="name")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password")



class Userregistrationform(forms.ModelForm):
    username = forms.CharField(max_length=50, label="name")
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Password-rpeat")

    class Meta:
        model = User
        fields = ("username", 'first_name', 'email')

    def clean_password2(self):
        data = self.cleaned_data
        if data["password"] != data["password2"]:
            raise forms.ValidationError("пароли не совпадают")
        return data["password2"]

    def clean_email(self):
        _email = self.cleaned_data["email"]
        email = validate(
            email_address= _email,
            check_format=True,
            check_blacklist=True,
            check_dns=True,
            dns_timeout=10,
            check_smtp=False,
            smtp_debug=False)
        if not email:
            raise forms.ValidationError("email не сушествует")
        if User.objects.filter(email=_email):
            raise forms.ValidationError("емайл уже сушествует")
        return _email



class Userupdateform(forms.ModelForm):
    name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput, label="Password-rpeat")

    class Meta:
        model = User
        fields = ("name","first_name", "last_name")

    def clean_password2(self):
        data = self.cleaned_data
        if data["password"] != data["password2"]:
            raise forms.ValidationError("пароли не совпадают")
        return data["password2"]

