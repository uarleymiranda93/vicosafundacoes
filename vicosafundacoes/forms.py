
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


# - Create/Register a user (Model Form)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        
        # Altera o widget do campo username
        username_attrs = {
            'class': 'form-control h-auto form-control-solid py-4 px-8',
            'placeholder': 'Digite seu nome de usuário'
        }
        self.fields['username'].widget = forms.TextInput(attrs=username_attrs)
        
        # Altera o widget do campo email
        email_attrs = {
            'class': 'form-control h-auto form-control-solid py-4 px-8',
            'placeholder': 'Digite seu endereço de e-mail'
        }
        self.fields['email'].widget = forms.EmailInput(attrs=email_attrs)
        
        # Altera o widget do campo password1
        password1_attrs = {
            'class': 'form-control h-auto form-control-solid py-4 px-8',
            'placeholder': 'Digite sua senha'
        }
        self.fields['password1'].widget = forms.PasswordInput(attrs=password1_attrs)

        # Modify widget attributes for password2
        password2_attrs = {
            'class': 'form-control h-auto form-control-solid py-4 px-8',
            'placeholder': 'Confirme sua senha'
        }
        self.fields['password2'].widget = forms.PasswordInput(attrs=password2_attrs)

        # Tradução dos labels dos campos
        self.fields['username'].label = 'Nome de usuário'
        self.fields['email'].label = 'Endereço de e-mail'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmação de senha'
        
        # Tradução dos textos de ajuda (helptext)
        self.fields['password1'].help_text = "Sua senha não pode ser muito semelhante às suas outras informações pessoais. Ela deve conter pelo menos 8 caracteres, não pode ser uma senha comum e não pode ser completamente numérica."
        self.fields['username'].help_text = "Obrigatório. 150 caracteres ou menos. Apenas letras, dígitos e @/./+/-/_ são permitidos."
        self.fields['password2'].help_text = "Digite a mesma senha que você digitou antes, para verificação."
    
        
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]
        error_messages = {
            'password_mismatch': "As senhas não coincidem.",
        }

    # Sobrescrever o método clean para personalizar a mensagem de erro
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            self.add_error('password2', "As senhas não coincidem.")
            self.fields['password2'].widget.attrs.update({'class': 'form-control is-invalid'})

        return cleaned_data


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())