from django.db import models
from django.contrib.auth.models import User

class PowerData(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.CharField(max_length=100)
    auth_key = models.CharField(max_length=20, min_length=20, label="Authentication Key Messtellenbetreiber")
    # Address start
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    # Address end
