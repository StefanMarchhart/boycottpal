from django.conf.urls import url
from . import views
import account
from django.contrib.auth import views as auth_views
from account.forms import LoginForm

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    # url(r'^logout/$', account.views.logout ),
    url(r'^logout/$', auth_views.logout, {'template_name': 'home.html', 'next_page': '/?alert=logout'}, name='logout'),
    url(r'^signup/$', views.Signup, name='signup'),
    url(r'^settings/$', account.views.change_email, name='change_email'),
    url(r'^settings/$', account.views.change_password, name='change_password'),
    url(r'^settings/$', account.views.settings, name='settings'),
    url(r'^reset/use/(?P<token>[A-Za-z0-9]+)', account.views.reset_password, name='reset_password'),
    url(r'^reset/get/$', account.views.get_reset, name='get_reset')
]
