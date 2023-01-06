from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
	
	username = models.SlugField("Username", max_length=256, unique=True, null=True)
	age = models.PositiveIntegerField("Age", null=True)
	phone = models.CharField("Phone", max_length=18)

	created_at = models.DateTimeField("Created at", auto_now_add=True)
	updated_at = models.DateTimeField("Updated_at", auto_now=True)

	USERNAME_FIELD = "username"
	first_name = None
	last_name = None


