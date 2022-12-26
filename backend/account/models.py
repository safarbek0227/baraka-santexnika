from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
	ADDRESS = (
		('Andijon', 'Andijon'),
		('Namangan', 'Namangan'),
		('Samarqand', 'Samarqand'),
		('Tashkent', 'Tashkent'),
		('Jizzax', 'Jizzax'),
		('Surxondaryo', 'Surxondaryo'),
		('Navoiy', 'Navoiy'),
		('Xorazm', 'Xorazm'),
		('Qashqadaryo', 'Qashqadaryo'),
		('Buxoro', 'Buxoro'),
		('Sirdaryo', 'Sirdaryo'),
		('Fargona', 'Fargona'),
	)
	
	name = models.CharField("Name", max_length=256)
	surname = models.CharField("Surname", max_length=256)
	username = models.SlugField("Username", max_length=256, unique=True, null=True)
	age = models.PositiveIntegerField("Age", null=True)
	phone = models.CharField("Phone", max_length=18)
	avatar = models.ImageField("Image", upload_to="user-images/", null=True, blank=True, default='default.png')
	address = models.CharField("Address", max_length=128, choices=ADDRESS)

	created_at = models.DateTimeField("Created at", auto_now_add=True)
	updated_at = models.DateTimeField("Updated_at", auto_now=True)

	USERNAME_FIELD = "username"
	first_name = None
	last_name = None


