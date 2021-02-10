from django import forms
from .models import ClassD

class ClassForm(forms.Form):
    class Meta:
        model = ClassD
        fields = ['title']
