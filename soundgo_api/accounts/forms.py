from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

import re

UserAccount = get_user_model()

pass_regex = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s)")


class UserAccountAdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=8, max_length=255,
                                help_text="At least 8 characters.<br/>At least one lowercase letter, one uppercase "
                                          "letter, one number and one special character.<br/>No white spaces.")
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ('nickname',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords dont' match.")
        elif password1 and password2 and not pass_regex.match(password2):
            raise forms.ValidationError("Invalid password format.")

        return password2

    def save(self, commit=True):
        user_account = super(UserAccountAdminCreationForm, self).save(commit=False)
        user_account.set_password(self.cleaned_data["password1"])
        if commit:
            user_account.save()
        return user_account


class UserAccountAdminChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserAccount
        fields = ('nickname', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]
