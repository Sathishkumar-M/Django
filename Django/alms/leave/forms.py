from django import forms
from django.contrib.auth.models import User
from leave.models import LeaveRules,LeaveApply
from django.conf import settings
import datetime
class LeaveRulesForm(forms.ModelForm):
    class Meta():
        model = LeaveRules
        fields = ('leave_type','leave_rules')

        widgets = {
            'leave_rules':forms.Textarea(attrs={'class':'editable'})
            }


class LeaveApplyForm(forms.ModelForm):
    start_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,widget=forms.DateInput(format='%d/%m/%Y',attrs={'class': 'fromDate'}))
    end_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,widget=forms.DateInput(format='%d/%m/%Y',attrs={'class': 'toDate'}))
    class Meta():
        model = LeaveApply
        fields = ('leave_type','start_date','end_date','notes','tag_to','no_of_days')

        widgets = {
            'no_of_days':forms.HiddenInput(attrs={'class':'no_of_days'})
            }
