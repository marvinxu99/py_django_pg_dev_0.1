from django.db import models
from django.conf import settings

from ..globals import POSITION_CD


class Prsnl(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        unique=True, 
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True},
    )
    prsnl_id = models.BigAutoField(primary_key=True, editable=False)

    is_active = models.BooleanField('Active', default=False)
    active_status_cd = models.IntegerField('Ative Status', default=1)

    name_first = models.CharField("Fist Name", max_length=128, blank=True)
    name_middle = models.CharField("Middle Name", max_length=128, blank=True)
    name_last = models.CharField("Last Name", max_length=128, blank=True)
    name_full_formatted = models.CharField("Full Name", max_length=128, blank=True)
    position = models.CharField(max_length=3, choices=POSITION_CD, default='N01')

    class Meta:
        verbose_name = "personnel"
        verbose_name_plural = "personnel"

    def __str__(self):
        return self.name_full_formatted


class Prsnl_Alias(models.Model):
    prsnl_alias_id = models.BigAutoField(primary_key=True, editable=False)
    prsnl = models.ForeignKey(Prsnl, on_delete=models.CASCADE)

    is_active = models.BooleanField('Active', default=1)
    active_status_cd = models.IntegerField('Ative Status', default=1)
    alias = models.CharField('Alias', max_length=200, default='abc')
    alias_expiry_dt_tm = models.DateTimeField("Alias Expiry Date", null=True, blank=True)
    alias_pool_cd = models.IntegerField('Alias Type', default=1)

    def __str__(self):
        return self.alias