from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Note

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Обязательно к заполнению')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
