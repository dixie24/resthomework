from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from users.managers import CustomUserManager 
from django.utils import timezone

class ConfirmationCode(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ConfirmationCode(user={self.user.email if self.user else 'No user'})" 

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    birthdate = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    objects = CustomUserManager()
    date_joined = models.DateTimeField(default=timezone.now) 
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    
    def __str__(self):
        return self.email or ''
