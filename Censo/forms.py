from django import forms
from .models import Censo

class CensoForm(forms.ModelForm):

    class Meta:
        model = Censo
        fields = '__all__'