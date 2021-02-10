from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from .forms import AssessForm
from .models import Assess
from timetable.models import ClassD


@login_required(login_url='common:login')
def create(request, class_id):
    classinfo = get_object_or_404(ClassD, pk=class_id)

    if request.method == 'POST':
        form = AssessForm(request.POST)
        if form.is_valid():
            assess = form.save(commit=False)
            assess.author = request.user
            assess.classinfo = classinfo
            assess.create_date = timezone.now()
            assess.save()
            return redirect('index')
    else:
        form = AssessForm()

    context = {'form': form, 'classinfo': classinfo}

    return render(request, 'assess_create.html', context)


@login_required(login_url='common:login')
def list(request):
    page = request.GET.get('page', '1')

    assess_list = Assess.objects.order_by('-create_date')

    paginator = Paginator(assess_list, 10)
    page_obj = paginator.get_page(page)

    context = {'assess_list': page_obj}
    return render(request, 'assess_list.html', context)

@login_required(login_url='common:login')
def detail(request, assess_id):
    assess = get_object_or_404(Assess, pk=assess_id)
    context = {'assess': assess}
    return render(request, 'assess_detail.html', context)


@login_required(login_url='common:login')
def delete(request, assess_id):
    assess = get_object_or_404(Assess, pk=assess_id)

    if request.user != assess.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('board:detail', assess_id=assess.id)

    assess.delete()

    return redirect('index')



