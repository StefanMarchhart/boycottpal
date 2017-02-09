from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from boycotted.models import Boycott
import datetime
# Create your models here.

class BoycottUser(AbstractUser):
    boycotts = models.ManyToManyField(Boycott, blank=True)
    zip = models.CharField(max_length=5,
                           null=True,
                           blank=True,
                           validators=[
                               RegexValidator(r'^\d{1,10}$',
                                              message="Please enter a valid zipcode")
                           ]
                           )

class Token(models.Model):
    user=models.ForeignKey(
        'account.BoycottUser'
    )
    token=models.CharField(max_length=500, verbose_name="Reset token")
    date= models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return 'Token: for' + self.user.username

class HC(models.Model):
    hits=models.IntegerField(default=0)
    def __str__(self):
        return 'Hits: ' + str(self.hits)