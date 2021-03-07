from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class PasswordModel(models.Model):
    account_name = models.CharField(max_length=200)
    password_value= models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.account_name
