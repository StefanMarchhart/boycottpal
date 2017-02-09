from django.db import models
import datetime

# Create your models here.
class Poll(models.Model):
    # Name of the person/place being boycotted
    name = models.CharField(max_length=500, verbose_name="The Name of the Poll")
    # Location of a local variant of the boycotted or null if it's a non-local thing

    # The boycotts filed against the boycotted object
    choices = models.ManyToManyField("polls.Choice", blank=True)
    voters = models.ManyToManyField("account.BoycottUser", blank=True)
    date= models.DateTimeField(default=datetime.datetime.now)
    color = models.CharField(max_length=200)
    def __str__(self):
        return 'Poll: ' + self.name

# This class represents an individual instance of a boycott. Think Grandma boycotting Obama
class Choice(models.Model):
    # The user doing the boycotting

    name = models.CharField(max_length=500, verbose_name="The Choice")
    votes = models.IntegerField(default=0)
    target = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.name

#