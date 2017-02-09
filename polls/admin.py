from django.contrib import admin


# Register your models here.
from polls.models import *

admin.site.register(Poll)
admin.site.register(Choice)

