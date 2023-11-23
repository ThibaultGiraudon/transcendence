from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, photo_url="https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png", **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, photo_url=photo_url, **extra_fields)
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
    photo_url = models.CharField(max_length=200)

    # Utilise le gestionnaire d'utilisateurs personnalisé
    objects = CustomUserManager()

    # Ajoute d'autres champs personnalisés si nécessaire

    class Meta:
        # Ajoute ces lignes pour résoudre les conflits d'accessoires inverses
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

def save(self, *args, **kwargs):
    super().save()