from django import forms
from django.core.validators import RegexValidator
from .models import CustomUser
from django.forms import FileInput

class LoginForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput)
	password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class SignUpForm(forms.Form):
	username = forms.CharField(
		max_length=65, 
		validators=[
			RegexValidator(
				regex='^[a-zA-Z0-9]*$', 
				message='Username must be Alphanumeric', 
				code='invalid_username'
			)
		]
	)
	email = forms.EmailField(widget=forms.EmailInput)
	password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
   
	class Meta:
		model = CustomUser
		fields = ['username', 'photo']
		widgets = {
			'photo': FileInput(),
		}
		validators={
			'username': [
				RegexValidator(
					regex='^[a-zA-Z0-9]*$', 
					message='Username must be Alphanumeric', 
					code='invalid_username'
				)
			]
		}
		
	def __init__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		# Add defaults values for attributes if needed
		self.fields['username'].label = "New username"