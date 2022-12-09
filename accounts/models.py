from django.db import models
from django.contrib.auth.models import AbstractUser


class Post(models.Model):
    title = models.CharField(max_length=300, unique=True)
    content = models.TextField()

class CustomUser(AbstractUser):
    miles = models.BooleanField(default=True)
