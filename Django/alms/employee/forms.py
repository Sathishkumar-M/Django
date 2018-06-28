from django import forms
from django.contrib.auth.models import User
from employee.models import EmployeeProfileInfo

class EmployeeForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name','email',)

class EmployeeProfileInfoForm(forms.ModelForm):
    class Meta():
        model = EmployeeProfileInfo
        fields = ('profile_pic','age','phone','address')

        widgets = {
            'phone':forms.TextInput(attrs={'class':'textinputclass'}),
            'address':forms.Textarea(attrs={'class':'editable'})
            }
