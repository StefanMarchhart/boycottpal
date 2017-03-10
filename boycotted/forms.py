from django import forms
from boycotted.models import Boycott, Boycotted, DirtyFilterModelIFeelGuiltyAbout, SORT_CHOICES


class BoycottedForm(forms.ModelForm):
    class Meta:
        model = Boycotted
        fields = ['name', 'zip', 'tag']
class AdminTagForm(forms.ModelForm):
    class Meta:
        model = Boycotted
        fields = ['tag']

class BoycottForm(forms.ModelForm):
    class Meta:
        model = Boycott
        fields = ['reason']

class FilterForm(forms.ModelForm):
    sort = forms.ChoiceField(choices=SORT_CHOICES, initial='',
                                        widget=forms.RadioSelect)
    class Meta:
        model = DirtyFilterModelIFeelGuiltyAbout
        fields = ['tag']
