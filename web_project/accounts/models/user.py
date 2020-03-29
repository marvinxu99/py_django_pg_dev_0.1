from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True, editable=False)
    first_name = None
    last_name = None