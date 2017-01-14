from django.db import models
from django.contrib.auth.models import AbstractUser
from boycotted.models import Boycott
# Create your models here.

class BoycottUser(AbstractUser):
    boycotts = models.ManyToManyField(Boycott, blank=True)