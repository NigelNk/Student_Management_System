from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model   = CustomUser
        fields  = ['email', 'username', 'first_name', 'last_name', 'role']

    
    def clean_email(self):
        email   = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email is already taken')
        
        return email
    
    def clean(self):
        cleaned_data  = super().clean()
        email = cleaned_data.get('email')

        if email and CustomUser.objects.filter(email=email, is_superuser=True).exists():
            cleaned_data['role'] = 'admin'
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)

        if CustomUser.objects.filter(email=user.email, is_superuser=True).exists():
            user.role = 'admin'
        
        if commit:
            user.save()

        return user
        
     
        

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model  = CustomUser
        fields = ['email', 'username',]
        

