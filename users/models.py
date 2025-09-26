from django.db import models
from django.contrib.auth.models import User
import random
import string


class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=6, unique=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.сode = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Код подтверждения"
        verbose_name_plural = "Коды подтверждения"
