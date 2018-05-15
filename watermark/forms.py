from django import forms
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Submit, Layout, Div, Fieldset


class UploadFileForm(forms.Form):
    image = forms.ImageField()
    CHOICES = (('visible', 'visible'), ('invisible', 'invisible'),)
    option = forms.ChoiceField(choices=CHOICES)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    watermark_image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    def clean(self):
        cleanded_data = super(UploadFileForm, self).clean()
        message = cleanded_data.get('message')


class Retrive(forms.Form):
    image = forms.ImageField()
    coverImage = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(Retrive, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
