from django import forms
from .models import Post, Response

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'content', 'options', 'visible']
        labels = {
            'subject': '제목',
            'content': '내용',
            'options': '선택지',
            'visible': '공개',
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['option']
        labels = {
            'content': '선택지',
        }
