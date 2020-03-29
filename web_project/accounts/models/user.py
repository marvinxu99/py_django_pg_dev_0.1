from django.contrib.auth.models import AbstractUser
from django.db import models
from .person import Person
from .prsnl import Prsnl


class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True, editable=False)
    first_name = None
    last_name = None

    def get_full_name(self):
        if self.is_staff:
            p = Prsnl.objects.filter(user=self)[0]
        else:
            p = Person.objects.filter(user=self)[0]
        return p.name_full_formatted
    get_full_name.admin_order_field = 'name_last'
    get_full_name.short_description = 'full name'
