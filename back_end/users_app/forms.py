from django import forms
from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    email = forms.EmailField()
    
class EditProfileForm(forms.ModelForm):
   
    class Meta:
            model = CustomUser
            fields = ['username']
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Ajoutez des attributs, des étiquettes, des classes CSS, etc., au besoin
        self.fields['username'].label = 'New Username'