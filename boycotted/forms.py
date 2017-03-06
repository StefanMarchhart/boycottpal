from django import forms
from boycotted.models import Boycott, Boycotted, DirtyFilterModelIFeelGuiltyAbout


class BoycottedForm(forms.ModelForm):
    class Meta:
        model = Boycotted
        fields = ['name', 'zip', 'tag']

class BoycottForm(forms.ModelForm):
    class Meta:
        model = Boycott
        fields = ['reason']

class FilterForm(forms.ModelForm):
    class Meta:
        model = DirtyFilterModelIFeelGuiltyAbout
        fields = ['tag','sort']
