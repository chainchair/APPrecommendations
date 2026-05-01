from django.db import models
from django.contrib.auth.models import AbstractUser

class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True)

    def __str__(self):
        return self.username
