from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Interest

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password_confirm
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class InteresesForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['interests']
        widgets = {
            'interests': forms.CheckboxSelectMultiple(),
        }