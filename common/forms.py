from django import forms
from CustomUser.forms import UserCreationForm
from CustomUser.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="email")
    student_name = forms.CharField(label="이름")
    student_number = forms.CharField(label="학번")

    class Meta:
        model = User
        fields = ("email", "student_name", "student_number")
