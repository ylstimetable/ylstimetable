from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from common.forms import UserForm
from django.urls import reverse_lazy
from django.contrib import messages
from CustomUser.models import User

INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

def logininto(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(email=username, password=password)
        if not user:
            messages.error(request, '존재하지 않는 계정이거나 비밀번호가 틀렸습니다.')
            return render(request, 'common/login.html')

        if user is not None:
            login(request, user)
            return redirect('index')
    else:
        return render(request, 'common/login.html')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            student_number = form.cleaned_data.get('student_number')
            student_name = form.cleaned_data.get('student_name')
            user = authenticate(email=email, password=raw_password, student_number=student_number,
                                student_name=student_name)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()

    return render(request, 'common/signup.html', {'form': form})


def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, 'common/404.html', {})


class UserPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('common:password_reset_done')
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'password_reset_done_fail.html')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy('common:password_reset_complete')
    template_name = 'password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context