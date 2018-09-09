from django import forms
from activities.models import Activities, Groups


class ActivitiesForm(forms.ModelForm):
    class Meta:
        model = Activities
        fields = ['short_name', 'links', 'begin', 'img']
        labels = {'short_name': "activity's name", 'links': 'link',
                  'begin': "when will your activity start", 'img': 'attach a picture'}

class GroupsForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['group_name', 'img']
        labels = {'group_name': "group's name", 'img': 'avatar'}
