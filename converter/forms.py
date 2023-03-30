from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот почтовый ящик уже используется.')
        return email



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=User.objects.get(email=username).username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid email or password')
            else:
                self.user_cache = user
                return self.cleaned_data


