from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Receipt, Reserve, Result
from random import shuffle
from datetime import datetime, timedelta

@login_required(login_url='common:login')
def create_receive(request):
    sem = request.POST.get("semester")
    a = Receipt(semester=sem)
    a.save()

    return redirect('libraryseat:index')


@login_required(login_url='common:login')
def receive(request):
    q = Receipt.objects.filter(semester='2022-2')
    for obj in q:
        q_obj = obj

    q_obj.voter.add(request.user)
    return redirect('libraryseat:index')



@login_required(login_url='common:login')
def random(request):
    applicant_list = Receipt.objects.filter(semester='2022-2')
    for obj in applicant_list:
        q = obj

    target= []

    for applicant in q.voter.all():
        target.append(applicant.student_number)

    shuffle(target)
    strings = ','.join(target)
    a = Result(semester='2022-2', sequence=strings, sequence_backup=strings)
    a.save()

    return redirect('libraryseat:index')


@login_required(login_url='common:login')
def register(request):
    result = Result.objects.filter(semester='2022-2')
    for re in result:
        result = re

    room_num = request.POST.get("room_num")
    room = int(room_num)

    check = Reserve.objects.filter(room=room).count

    if request.user.student_number != result.current:
        messages.error(request, "현재 예약 대상이 아닙니다.")
        return redirect('libraryseat:index')

    if check != 0:
        a = Reserve(author=request.user, room=room)
    else:
        messages.error(request, '이미 해당 시간에 예약이 존재합니다.')

    return redirect('libraryseat:index')



@login_required(login_url='common:login')
def index(request):
    return render(request, 'libraryseat.html')








