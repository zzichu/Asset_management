from django.db import models
from django.utils import timezone

class item(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    itemName = models.CharField(max_length=8)
    name = models.CharField(max_length=4)
    team = models.CharField(max_length=4)
    status = models.CharField(max_length=2, null=True, default=None, blank=True)
    register_date = models.DateField(default=timezone.now)
    rental_date = models.DateField(null=True, default=None)
    return_date = models.DateField(null=True, default=None)