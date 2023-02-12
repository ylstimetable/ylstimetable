from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import datetime

from django.core.paginator import Paginator

#from .forms import PostForm, ResponseForm
from .models import Post, Response


@login_required(login_url='common:login')
def list(request):
    user = request.user

    if user.student_auth == False:
        return render(request, 'unauth.html')

    page = request.GET.get('page', '1')

    post_list = Post.objects.order_by('-end_day')

    paginator = Paginator(post_list, 10)
    page_obj = paginator.get_page(page)

    context = {'survey_list': page_obj}
    return render(request, 'survey_list.html', context)
  
  

@login_required(login_url='common:login')
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    questions = post.question_set.all()
    options = []
    for q in questions:
        options.append(q.get_choices())
    context = {'post': post, 'qao': zip(questions, options)}
    return render(request, 'survey_detail.html', context)



@login_required(login_url='common:login')
def receive(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    q = Response.objects.filter(post=post)
    q_obj = None
    for obj in q:
        q_obj = obj
    if q_obj and request.user in q_obj.author.all():
        temp_error_message = '이미 접수된 사용자입니다.'
        return redirect('survey:list')
    post.response_set.create(author=request.user, post=post)
    '''
    for key in request.POST:
        print(key)
        value = request.POST[key]
        print(value)
    floor = request.POST.get("floor")
    student_fee = request.POST.get("student_fee")
    smoke = request.POST.get("smoke")

    q = Response.objects.filter(post='2023-1')
    for obj in q:
        q_obj = obj

    if request.user in q_obj.voter.all():
        stored_user = Receipt_Student.objects.get(author=request.user)
        temp_error_message = '이미 접수된 사용자입니다. 학생회비 납부 여부: {}; 선호층: {}; 흡연여부: {}'.format(stored_user.fee, stored_user.floor, stored_user.smoke)
        messages.error(request, temp_error_message)
        return redirect('libraryseat:index')
    else:
        messages.success(request, '접수 완료되었습니다.')
        q_obj.voter.add(request.user)
        a = Receipt_Student(author=request.user, student_number = request.user.student_number, fee=student_fee, floor=floor, smoke=smoke)
        a.save()
    '''
    return redirect('survey:list')
