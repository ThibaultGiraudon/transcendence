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

	def clean(self):
		cleaned_data = super().clean()
		username = cleaned_data.get('username')
		email = cleaned_data.get('email')

		if CustomUser.objects.filter(email=email).exists():
			self.add_error('email', "This email is already taken")

		if CustomUser.objects.filter(username=username).exists():
			self.add_error('username', "This username is already taken")

		if len(username) < 4:
			self.add_error('username', 'Your username is too short (4 characters minimum)')

		return cleaned_data


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