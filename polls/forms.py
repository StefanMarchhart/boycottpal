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

