from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Avatar

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-mail")
    username = forms.CharField(label="Nombre de Usuario")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput)
    birth_date = forms.DateField(label="Fecha de Nacimiento", widget=forms.SelectDateWidget(years=range(1900, 2023)), error_messages={'required': 'Este campo es obligatorio.', 'invalid': 'Ingrese una fecha válida.'})


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'birth_date']
        help_texts = {k:"" for k in fields}

class UserEditForm(UserCreationForm):
    email = forms.EmailField(label="Modificar E-mail")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        #Saca los mensajes de ayuda
        help_texts = {k:"" for k in fields}


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']
