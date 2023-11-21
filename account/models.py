from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from phone_field import PhoneField

class MyUser(AbstractUser):
	email=models.EmailField(max_length=200,unique=True)
	is_author=models.BooleanField(default=True)
	profile_image=models.ImageField(upload_to='profile_image/%Y/',null=True)


class UserInfo(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	title=models.CharField(max_length=200)
	description=models.TextField(blank=True)
	phone = PhoneField(blank=True, help_text='Contact phone number')
	LinkedIn =models.URLField(blank=True)
	address=models.TextField(blank=True)


class Portfolio(models.Model):
	user_info=models.ForeignKey(UserInfo,on_delete=models.CASCADE,related_name='portfolio')
	title=models.CharField(max_length=200)
	description=models.TextField(blank=True)
	website=models.URLField(blank=True)


