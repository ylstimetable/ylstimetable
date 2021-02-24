from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.core.paginator import Paginator

from .forms import AnnounceForm
from .models import Announce

@login_required(login_url='common:login')
def list(request):
    page = request.GET.get('page', '1')

    announce_list = Announce.objects.order_by('-create_date')

    paginator = Paginator(announce_list, 10)
    page_obj = paginator.get_page(page)

    context = {'announce_list': page_obj}
    return render(request, 'commonboard_list.html', context)


@login_required(login_url='common:login')
def detail(request, announce_id):
    announce = get_object_or_404(Announce, pk=announce_id)
    context = {'announce': announce}
    return render(request, 'commonboard_detail.html', context)


@login_required(login_url='common:login')
def announce_create(request):
    if request.method == 'announce':
        form = AnnounceForm(request.announce)
        if form.is_valid():
            announce = form.save(commit=False)
            announce.author = request.user
            announce.create_date = timezone.now()
            announce.save()
            return redirect('commonboard:list')
    else:
        form = AnnounceForm()

    context = {'form': form}

    return render(request, 'commonboard_create.html', context)


@login_required(login_url='common:login')
def announce_modify(request, announce_id):
    announce = get_object_or_404(Announce, pk=announce_id)

    if request.user != announce.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('commonboard:list', announce_id=announce_id)

    if request.method == "announce":
        form = AnnounceForm(request.announce, instance=announce)
        if form.is_valid():
            announce = form.save(commit=False)
            announce.author = request.user
            announce.modify_date = timezone.now()
            announce.save()
            return redirect('', announce_id=announce_id)
    else:
        form = AnnounceForm(instance=announce)

    context = {'form': form}
    return render(request, 'commonboard_list.html', context)


@login_required(login_url='common:login')
def announce_delete(request, announce_id):
    announce = get_object_or_404(Announce, pk=announce_id)

    if request.user != announce.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('commonboard:list', announce_id=announce.id)

    announce.delete()

    return redirect('commonboard:list')
