from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from CustomUser.models import User


@staff_member_required(login_url='common:login')
def index(request):
    user = request.user

    if user.student_auth == False:
        return render(request, 'unauth.html')

    unauth_users = User.objects.filter(student_auth=False)
    existence = []

    for user in unauth_users:
        existence_user = User.objects.filter(student_auth=True).filter(student_number=user.student_number).exists()
        existence.append(existence_user)

    return render(request, 'studentauth.html', {"unauthusers": unauth_users, "existence": existence})


def register(request, user_id):
    auth_user = get_object_or_404(User, pk=user_id)
    auth_user.student_auth = True
    auth_user.save()
    return redirect('index')
