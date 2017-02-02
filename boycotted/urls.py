from django.conf.urls import url
# from . import views
from boycotted.views import *

urlpatterns = [
    url(r'^boycott/add/', AddBoycott, name='AddBoycott'),
    url(r'^boycott/edit/(?P<boycott_id>[0-9]+)', EditBoycott, name='EditBoycott'),
    url(r'^boycotted/view/(?P<boycotted_id>[0-9]+)', ViewBoycotted),
    url(r'^boycott/delete/(?P<boycott_id>[0-9]+)', DeleteBoycott)
]