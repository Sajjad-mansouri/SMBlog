from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
	email=models.EmailField(max_length=200,unique=True)
	is_author=models.BooleanField(default=False)

