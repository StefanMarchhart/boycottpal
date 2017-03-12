from django.core.validators import RegexValidator
from account.models import *
import datetime

# Create your models here.
TAG_CHOICES = (
    (1, ("Other")),
    (2, ("People")),
    (3, ("Sports")),
    (4, ("Buisnesses")),
    (5, ("International")),
    (6, ("Local"))
)

FILTER_TAG_CHOICES = (
    (1, ("All")),
    (2, ("Other")),
    (3, ("People")),
    (4, ("Sports")),
    (5, ("Buisnesses")),
    (6, ("International")),
    (7, ("Local"))
)

SORT_CHOICES = (
    (1, ("Most Boycotted")),
    (2, ("Alphabetical Order")),
    (3, ("Most Recent")),
)


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
    date = models.DateTimeField(default=datetime.datetime.now)
    tag = models.IntegerField(default=1, choices=TAG_CHOICES)
    comment_count = models.IntegerField(default=0)

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
        return 'Target: ' + self.target.name + ' - Boycotter: ' + self.boycotter.username + ' - Reason: ' + self.reason


class DirtyFilterModelIFeelGuiltyAbout(models.Model):
    tag = models.IntegerField(default=0, choices=FILTER_TAG_CHOICES)
    sort = models.IntegerField(default=0, choices=SORT_CHOICES)
