from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
# Create your views here.
from account.views import _get_disqus_sso
from boycott.general import custom_strftime
from polls.forms import PollForm, NewPollForm
from polls.models import *

def ViewPoll(request,poll_id):
    # if this is a POST request we need to process the form data
    poll=Poll.objects.get(id=poll_id)
    labels=[]
    data=[]
    color=poll.color.split(',')
    for choice in poll.choices.all():
        labels.append(choice.name)
        data.append(choice.votes)

    # decoded_json = json.loads(json.dumps(boycotts))

    disqus_sso = _get_disqus_sso(request.user)



    return render(request, 'view_poll.html', {
        'name': poll.name,
        'labels': labels,
        'data': data,
        'color': color,
        'id': poll_id,
        'date': custom_strftime('%B {S}', poll.date),
        "disqus_sso": disqus_sso
    })


def ViewAllPolls(request):
    all_polls=[]
    polls=Poll.objects.all().order_by('-date')
    for poll in polls:
        pol= {
            'name':poll.name,
            'id':poll.id,
            'date':custom_strftime('%B {S}', poll.date)
        }
        all_polls.append(pol)

    return render(request, 'view_all_poll.html', {
        'all_polls': all_polls
    })
@login_required(login_url='/login/')
def VotePoll(request,poll_id):
    poll=Poll.objects.get(id=poll_id)
    if request.user in poll.voters.all():
        return HttpResponseRedirect('/poll/view/' + poll_id)
    num_choices = poll.choices.all().count()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        poll_form = PollForm(data=request.POST, id=poll_id)
        if poll_form.is_valid():
            poll_output=poll_form.save(commit=False)
            vote = poll_form.cleaned_data['choice']
            vote.votes+=1
            vote.save()
            poll.voters.add(request.user)
            poll.save()

            return HttpResponseRedirect('/poll/view/'+poll_id)



    else:
        poll_form = PollForm(id=poll_id)

    return render(request, 'vote_poll.html', {
        'poll_form':poll_form,
        'id':poll_id,
        'name':poll.name,
        'num_choices':num_choices
    })

@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def MakePoll(request,):
    if request.method == 'POST':
        poll_form = NewPollForm(data=request.POST)
        if poll_form.is_valid():
            color=poll_form.cleaned_data['color']

            name=poll_form.cleaned_data['name']
            poll_obj=Poll.objects.create(name=name)
            poll_obj.color=color
            choices=[
                poll_form.cleaned_data['choice0'],
                poll_form.cleaned_data['choice1'],
                poll_form.cleaned_data['choice2'],
                poll_form.cleaned_data['choice3'],
                poll_form.cleaned_data['choice4'],
                poll_form.cleaned_data['choice5'],
                poll_form.cleaned_data['choice6'],
                poll_form.cleaned_data['choice6']

            ]
            counter=0
            for option in choices:
                if option !='':
                    choice_obj=Choice.objects.create(name=option, target=poll_obj)
                    poll_obj.choices.add(choice_obj)
                    counter+=1
            poll_obj.save()

            return HttpResponseRedirect('/console/?alert=poll')



    else:
        poll_form = NewPollForm()

    return render(request, 'console.html', {
        'poll_form':poll_form
    })

@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def DeletePoll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')
    poll.delete()

    return HttpResponseRedirect('/')