from django import forms
from django.db import models

class EuDateFormField(forms.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.update({'input_formats': ('%d/%m/%Y %H:%M',)})
        super(EuDateFormField, self).__init__(*args, **kwargs)

class EuDateField(models.DateTimeField):
    def formfield(self, **kwargs):
        kwargs.update({'form_class': EuDateFormField})
        return super(EuDateField, self).formfield(**kwargs)