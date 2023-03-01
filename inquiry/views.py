from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import datetime

from django.utils import timezone
from django.core.paginator import Paginator

from .models import Post


  

@login_required(login_url='common:login')
def write(request):
    
    return render(request, 'inquiry.html')



@login_required(login_url='common:login')
def receive(request):

    content = request.POST.get("content")
    print(content)
    
    post = Post(content=content)
    post.create_date = timezone.now()
    post.save()
    

    messages.success(request, '문의가 접수되었습니다.')

    return redirect('inquiry:write')
