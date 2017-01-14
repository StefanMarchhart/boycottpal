from django.contrib import admin

# Register your models here.
from boycotted.models import *

admin.site.register(Boycott)
admin.site.register(Boycotted)

