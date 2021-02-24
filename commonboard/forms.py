from django import forms
from .models import Announce

class AnnounceForm(forms.ModelForm):
    class Meta:
        model = Announce
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }
