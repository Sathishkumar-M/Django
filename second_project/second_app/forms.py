from django import forms
from django.core import validators
from second_app.models import User

class NameForm(forms.ModelForm):
    class Meta():
        model = User
        fields = '__all__'

# def check_z_name(value):
#     if value[0] != 'z':
#         raise forms.ValidationError('Name should be start with z ')

# class NameForm(forms.Form):
    # name = forms.CharField(validators=[check_z_name])
    # email = forms.EmailField()
    # verify_email = forms.EmailField(label='Enter your mail again:')
    # text = forms.CharField(widget=forms.Textarea)
    # botcatcher = forms.CharField(required=False,widget=forms.HiddenInput,validators=[validators.MaxLengthValidator(0)])

    # def clean_botcatcher(self):
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError('Gotcha bot!')
    #     return botcatcher

    # def clean(self):
    #     all_data = super().clean()
    #     email = all_data['email']
    #     vemail = all_data['verify_email']
    #
    #     if email != vemail:
    #         raise forms.ValidationError('Mail is not matched')
