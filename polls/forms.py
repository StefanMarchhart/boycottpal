from polls.models import Poll
from django import forms

class PollForm(forms.ModelForm):
    def __init__(self, id, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        self.fields['choice'].queryset = Poll.objects.get(id=id).choices.all()

    choice = forms.ModelChoiceField(queryset=Poll.objects.all(), empty_label=None,
                                        widget=forms.RadioSelect)
    class Meta:
        model = Poll
        fields = ['id']

class NewPollForm(forms.ModelForm):
    name = forms.CharField(required=True)
    choice0 = forms.CharField(required=True)
    choice1 = forms.CharField(required=True)
    choice2 = forms.CharField(required=False)
    choice3 = forms.CharField(required=False)
    choice4 = forms.CharField(required=False)
    choice5 = forms.CharField(required=False)
    choice6 = forms.CharField(required=False)
    color = forms.CharField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Poll
        fields = ['name','color']