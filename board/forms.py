from django import forms
from .models import Assess

class AssessForm(forms.ModelForm):
    class Meta:
        model = Assess
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }
