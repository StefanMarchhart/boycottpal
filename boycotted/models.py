from django.core.validators import RegexValidator
from account.models import *
import datetime
# Create your models here.

# This model describes an entity being boycotted i.e. Trump or My local applebee's
class Boycotted(models.Model):
    # Name of the person/place being boycotted
    name = models.CharField(max_length=500, verbose_name="Entity being boycotted")
    # Location of a local variant of the boycotted or null if it's a non-local thing
    zip = models.CharField(max_length=5,
                           null=True,
                           blank=True,
                           validators=[
                               RegexValidator(r'^\d{1,10}$',
                                              message="Please enter a valid zipcode")
                           ]
                           )
    # The boycotts filed against the boycotted object
    boycotts = models.ManyToManyField("boycotted.Boycott", blank=True)
    date= models.DateTimeField(default=datetime.datetime.now)
    def __str__(self):
        return 'Boycotted: ' + self.name


# This class represents an individual instance of a boycott. Think Grandma boycotting Obama
class Boycott(models.Model):
    # The user doing the boycotting
    boycotter = models.ForeignKey(
        'account.BoycottUser',
        on_delete=models.CASCADE
    )
    # The time/date the boycott was submitted
    date = models.DateTimeField(default=datetime.datetime.now)
    # The reason for the boycott
    reason = models.CharField(max_length=500, verbose_name="Why are you boycotting?")
    # Target, not sure if needed yet
    target = models.ForeignKey(
        Boycotted,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return 'Boycott: ' + self.boycotter.username

#
