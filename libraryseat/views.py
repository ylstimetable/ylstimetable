from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Receipt, Reserve, Result
from random import shuffle
import datetime

@login_required(login_url='common:login')
def create_receive(request):
    sem = request.POST.get("semester")
    a = Receipt(semester=sem)
    a.save()

    return redirect('libraryseat:index')

@login_required(login_url='common:login')
def seat_admin(request):
    return render(request, 'libraryseat_admin.html')


@login_required(login_url='common:login')
def receive(request):
    q = Receipt.objects.filter(semester='2022-2')
    for obj in q:
        q_obj = obj

    if request.user in q_obj.voter.all():
        messages.error(request, '이미 접수된 사용자입니다.')
        return redirect('libraryseat:index')
    else:
        messages.success(request, '접수 완료되었습니다.')
        return redirect('libraryseat:index')


@login_required(login_url='common:login')
def random(request):
    r_all = Result.objects.all()
    next_semester = '2022-2'

    semester_list = []

    for r in r_all:
        semester_list.append(r.semester)

    if next_semester in semester_list:
        messages.error(request, '이미 랜덤배정이 완료되었습니다.')
        return redirect('libraryseat:index')

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
    result = Result.objects.filter(semester='2022-2')
    receipt_start = len(Receipt.objects.filter(semester='2022-2'))
    location = 10000
    random_start = 0

    if len(Result.objects.filter(semester='2022-2')) == 0:
        return render(request, 'libraryseat.html', {'location': location,
                                                    'random_start': random_start, 'receipt_start': receipt_start})
    else:
        for re in result:
            result = re

        list = result.sequence.split(',')
        random_start = 1


        if request.user.student_number in list:
            location = list.index(request.user.student_number)

        return render(request, 'libraryseat.html', {'location': location,
                                                    'random_start': random_start, 'receipt_start': receipt_start})

@login_required(login_url='common:login')
def reserve_status(request):
    q_all = Reserve.objects.all()

    seat_num = []
    seat_name = []
    ran = range(0,60)
    rang = range(1,6)

    for q in q_all:
        seat_name.append(q.author.student_name)
        seat_num.append(int(q.room))


    return render(request, 'libraryseat_status.html', {"seat_num": seat_num,
                                                       "seat_name": seat_name, "ran": ran, "rang": rang})

@login_required(login_url='common:login')
def seat_register(request):
    requested_seat = int(request.POST.get("seat_number"))
    current_queue = Result.objects.filter(semester='2022-2')
    for q in current_queue:
        current_queue = q

    q_all = Reserve.objects.all()
    reserved_seat = []
    reserved_user = []

    for q in q_all:
        reserved_seat.append(int(q.room))

    if request.user.student_number == current_queue.current:
        if request.user in reserved_user:
            messages.error()
        if requested_seat in reserved_seat:
            messages.error(request, '이미 예약된 좌석입니다.')
            return redirect('libraryseat:reserve_status')
        else:
            reserve = Reserve(author=request.user, room=requested_seat)
            reserve.save()
            messages.success(request, '예약이 완료되었습니다.')
            return redirect('libraryseat:reserve_status')
    else:
        messages.error(request, '현재 예약 순번이 아닙니다.')
        return redirect('libraryseat:reserve_status')






