from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.files import File
from django.conf import settings

class CustomUserManager(BaseUserManager):
	def create_user(self, email, username, password=None, photo=None, **extra_fields):
		
		if not email:
			raise ValueError('The Email field must be set')
		email = self.normalize_email(email)
		
		user = self.model(email=email, username=username, **extra_fields)

		if photo is None:
			with open(settings.DEFAULT_IMAGE_PATH, 'rb') as default_image_file:
				user.photo.save('default.jpg', File(default_image_file), save=False)
		else:
			user.photo = photo
		
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		return self.create_user(email, username, password=password, **extra_fields)


class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=150, unique=True)
	photo = models.ImageField(upload_to='static/users_app/img', default='default.jpg')
	channels = models.JSONField(default=dict)
	messages = models.JSONField(default=dict)

	# Use the custom manager
	objects = CustomUserManager()

	class Meta:
		# Allow to change the AUTH_USER_MODEL in settings.py
		swappable = 'AUTH_USER_MODEL'

	def __str__(self):
		return self.username

	def save(self, *args, **kwargs):
		super(CustomUser, self).save(*args, **kwargs)