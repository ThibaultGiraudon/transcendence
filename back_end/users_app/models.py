from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
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

    # Utilise le gestionnaire d'utilisateurs personnalisé
    objects = CustomUserManager()

    # Ajoute d'autres champs personnalisés si nécessaire

    class Meta:
        # Ajoute ces lignes pour résoudre les conflits d'accessoires inverses
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username
    