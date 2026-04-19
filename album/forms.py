from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class PhotoUploadForm(forms.Form):
    name = forms.CharField(max_length=40)
    image = forms.ImageField()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("A jelszavak nem egyeznek!")
        if p1:
            validate_password(p1)
        return cleaned

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Foglalt felhasználónév!")
        return username