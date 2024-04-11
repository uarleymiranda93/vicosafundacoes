
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        
        # Altera o widget do campo username
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome de usuário'})
        
        # Altera o widget do campo email
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu endereço de e-mail'})
        
        # Altera o widget do campo password1
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'})
        
        # Altera o widget do campo password2
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]
        labels = {
            'username': 'Nome de usuário',
            'email': 'Endereço de e-mail',
            'password1': 'Senha',
            'password2': 'Confirmação de senha',
        }
        error_messages = {
            'password_mismatch': "As senhas não coincidem.",
        }
# - Authenticate a user (Model Form)

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())