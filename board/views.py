from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from .models import ClassA, ClassA_Post
from timetable.models import ClassD


@login_required(login_url='common:login')
def create(request, classa_id):
    classa = get_object_or_404(ClassA, pk=classa_id)

    rate = request.POST.get("rate")
    content = request.POST.get("content")
    semester = request.POST.get("semester")


    n = ClassA_Post(classinfo=classa, subject=classa.subject, content=content, professor=classa.professor,
                        semester=semester, rate=rate, create_date=timezone.now())
    n.save()
    num = classa.classa_post_set.count()
    total = classa.classa_post_set.all()
    sum = 0
    for tot in total:
        sum = sum + float(tot.rate)

    classa.rate = sum/num
    classa.save()

    return redirect('board:list')


@login_required(login_url='common:login')
def create_tool(request, classa_id):
    classa = get_object_or_404(ClassA, pk=classa_id)
    context = {'classinfo': classa}

    return render(request, 'assess_createtool.html', context)


@login_required(login_url='common:login')
def list(request):

    user = request.user

    if user.student_auth == False:
        return render(request, 'unauth.html')

    page = request.GET.get('page', '1')

    recent_post = ClassA_Post.objects.all()
    recent_post = recent_post.order_by('-create_date')[:5]

    context = {'assess_list': recent_post}
    return render(request, 'assess_list.html', context)

@login_required(login_url='common:login')
def detail(request, classa_id):
    classinfo = get_object_or_404(ClassA, pk=classa_id)
    assess = classinfo.classa_post_set.all()
    assess = assess.order_by('-create_date')
    context = {'assess_list': assess, 'classinfo': classinfo}
    return render(request, 'assess_detail.html', context)


@login_required(login_url='common:login')
def result(request):
    if request.method == 'POST':
        name = request.POST.get("classname")
        class_list = ClassA.objects.all()
        classfind = class_list.filter(
            Q(subject__icontains=name) |
            Q(professor__icontains=name)
        ).distinct

    else:
        return render(request, 'assess_list.html')

    context = {'lists': classfind}
    return render(request, 'assess_result.html', context)

