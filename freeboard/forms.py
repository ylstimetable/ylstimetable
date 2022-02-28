from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'content', 'delete_unavailable']
        labels = {
            'subject': '제목',
            'content': '내용',
            'delete_unavailable': '삭제금지',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }