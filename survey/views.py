from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import datetime

from django.utils import timezone
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
        
    responded = False
    rs = post.response_set.all() 
    for r in rs:
        if not post.visible:
            temp_error_message = '응답이 마감된 설문입니다.\n'
            messages.error(request, temp_error_message)
            return redirect('survey:list')
        elif r.author.id == request.user.id:
            print(timezone.localtime().month)
            temp_error_message = '이미 응답한 설문입니다.\n'
            #messages.error(request, temp_error_message)
             
            qs = r.post.question_set.all()
            aas = r.get_clean_answers()
            for q, a in zip(qs, aas):
                temp_error_message += ("{}: {}; ".format( q, a ))
            messages.error(request, temp_error_message)
            
            return redirect('survey:list')
            
    context = {'post': post, 'qao': zip(questions, options), 'responded': responded}
    return render(request, 'survey_detail.html', context)



@login_required(login_url='common:login')
def receive(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    temp_res = []
    for q in post.question_set.all(): 
        print(q.subject)
        print(request.POST)
        temp_res.append(request.POST.get(q.subject))
    content=",".join(temp_res)
    
    post.response_set.create(author=request.user, post=post, content=content)
    
    return redirect('survey:list')
