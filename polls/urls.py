from django.conf.urls import url
# from . import views
from polls.views import *

urlpatterns = [
    url(r'^poll/view/all', ViewAllPolls),
    url(r'^poll/view/(?P<poll_id>[0-9]+)', ViewPoll),
    url(r'^poll/vote/$', ViewAllPolls),
    url(r'^poll/vote/(?P<poll_id>[0-9]+)', VotePoll, name='VotePoll')


    # url(r'^poll/answer/(?P<poll_id>[0-9]+)', polls.views.AnswerPoll)
]
