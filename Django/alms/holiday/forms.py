from django import forms
from django.contrib.auth.models import User
from holiday.models import Holiday
from django.conf import settings
import datetime

class HolidayForm(forms.ModelForm):
    # holiday_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,widget=forms.TextInput(attrs={'class': 'datePicker'}))
    holiday_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,widget=forms.DateInput(format='%d/%m/%Y',attrs={'class': 'datePicker'}))
    class Meta():
        model = Holiday
        fields = ('holiday_date','holiday_name','holiday_type','holiday_icon','note')

        # widgets = {
        #     'holiday_name':forms.TextInput(attrs={'class':'textinputclass'}),
        #     'holiday_date':forms.DateField(attrs={'class':'datePicker'}),
        #     }
