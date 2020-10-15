from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

# class UserLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserLoginForm, self).__init__(*args, **kwargs)

#     username = forms.EmailField(widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Kullanıcı adı', 'id': 'hello'}))
#     password = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Şifre',
#             'id': 'hi',
#         }
# ))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=(""),
        widget=forms.TextInput(attrs={'class' : 'myfieldclass','placeholder' : 'E-mail'}),
        help_text=False)
    password1 = forms.CharField(
        label=(""),
        strip=False,
        help_text=False,
        widget=forms.PasswordInput(attrs={'class' : 'myfieldclass','placeholder' : 'Şifre'}),
    )
    password2 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={'class' : 'myfieldclass','placeholder' : 'Şifre doğrula'}),
        strip=False,
        help_text=False,
    )
    username = forms.CharField(
        label=(""),
        widget=forms.TextInput(attrs={'class' : 'myfieldclass','placeholder' : 'Kullanıcı adı'}),
        strip=False,
        help_text=False,
        
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        