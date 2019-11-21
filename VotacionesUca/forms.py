import io
from django import forms
from UsuarioUca.models import UsuarioUca

import csv

class DataForm(forms.Form):
    data_file = forms.FileField()

    def clean_data_file(self):
        f = self.cleaned_data['data_file']

        if f:
            ext = f.name.split('.')[-1]
            if ext != 'csv':
                raise forms.ValidationError('Tipo de formato no soportado')
        return f

    def process_data(self):
        f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(f)

        for user in reader:
            UsuarioUca.objects.create_user(nif=user['nif'], email=user['email'] ,first_name=user['firstname'], last_name=user['lastname'], password=user['password'],
                                           is_staff=user['isstaff'], is_superuser=user['issuperuser'], is_active=user['isactive'])