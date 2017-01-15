from django.conf.urls import url
from . import views
import boycotted

urlpatterns = [
    url(r'^boycott/add/', boycotted.views.AddBoycott, name='AddBoycott'),
    # url(r'^boycott/edit/(?P<appt_id>[0-9]+)', boycotted.views.EditBoycott),
    url(r'^boycotted/view/(?P<boycotted_id>[0-9]+)', boycotted.views.ViewBoycotted),
    # url(r'^boycott/delete/(?P<appt_id>[0-9]+)', boycotted.views.DeleteBoycott)
]