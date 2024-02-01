from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):


    username = forms.CharField(
        max_length=50,
        required=True,
        label="",
        # help_text='E.g   07200200200 or 01200200200',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone Number.  ie 071001000",
            }
        ),
    )

    # first_name = forms.CharField(max_length=30, required=False,
    #     label='', help_text='Optional',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'First name...'
    #     }))

    # last_name = forms.CharField(max_length=30, required=False,
    #     label='', help_text='Optional',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Last name...'
    #     }))

    # phone_number = forms.CharField(max_length=150, required=True,
    #     label='',
    #     help_text='E.g   07200200200 or 01200200200',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Phone Number...'
    #     }))

    email = forms.EmailField(
        max_length=254,
        required=True,
        label="",
        #  help_text='Required.Enter valid email.Required wen if you forot password.',
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email..."}
        ),
    )

    # referer_code = forms.CharField(
    #     max_length=150,
    #     required=False,
    #     label="",
    #     # help_text='Dont have ? Enter ADMIN',
    #     # widget=forms.TextInput(
    #     #     attrs={"class": "form-control", "placeholder": "Referer Code"}
    #     # ),
    # )

    password1 = forms.CharField(
        required=True,
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password..."}
        ),
    )

    password2 = forms.CharField(
        required=True,
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm password..."}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")




# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("phone_number", "email")        
