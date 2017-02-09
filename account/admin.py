from django.contrib import admin

# Register your models here.
from account.models import *

admin.site.register(BoycottUser)
admin.site.register(Token)
admin.site.register(HC)

