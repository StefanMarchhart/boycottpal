from django.db import models
from django.contrib.auth.models import AbstractUser
from boycotted.models import Boycott
import datetime
# Create your models here.

class BoycottUser(AbstractUser):
    boycotts = models.ManyToManyField(Boycott, blank=True)

class Token(models.Model):
    user=models.ForeignKey(
        'account.BoycottUser'
    )
    token=models.CharField(max_length=500, verbose_name="Reset token")
    date= models.DateTimeField(default=datetime.datetime.now)
