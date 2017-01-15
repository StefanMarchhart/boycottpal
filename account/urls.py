from django.conf.urls import url
from . import views
import account
from django.contrib.auth import views as auth_views
from account.forms import LoginForm

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    # url(r'^logout/$', account.views.logout ),
    url(r'^logout/$', auth_views.logout, {'template_name': 'home.html', 'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.Signup, name='signup')
]
