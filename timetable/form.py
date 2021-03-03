from django import forms
from .models import ClassD, ClassM

class ClassForm(forms.Form):
    class Meta:
        model = ClassD
        fields = ['title']

class ClassmForm(forms.Form):
    class Meta:
        model = ClassM
        fields = ['title']