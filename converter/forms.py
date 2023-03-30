from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate



from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот почтовый ящик уже используется.')
        return email




class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(required=True)

    def clean_username(self):
        return self.cleaned_data['username'].lower()

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            try:
                user = authenticate(username=User.objects.get(email=username).username, password=password)
                if user is None:
                    raise forms.ValidationError('Неправильный email или пароль')
                else:
                    self.user_cache = user
                    return self.cleaned_data
            except User.DoesNotExist:
                raise forms.ValidationError('Неправильный email или пароль')
        return super().clean()


