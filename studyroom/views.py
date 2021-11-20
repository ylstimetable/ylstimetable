from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Reserve


@login_required(login_url='common:login')
def index(request, room_num):
    user = request.user
    q = Reserve.objects.filter(room = room_num)
    ran = range(1, 13)
    rang = range(0, 7)
    tabletime = []

    for temp in q:
        temptime = temp.time
        strings = temptime.split(',')
        count = 0

        for string in strings:
            string = string.replace(u'\xa0', u'')
            if len(string) == 3:
                if string[0] == '월':
                    tabletime.append(int(string[1]) * 10 + int(string[2]))
                    count = 0
                if string[0] == '화':
                    tabletime.append(int(string[1]) * 10 + int(string[2]) + 20)
                    count = 20
                if string[0] == '수':
                    tabletime.append(int(string[1]) * 10 + int(string[2]) + 40)
                    count = 40
                if string[0] == '목':
                    tabletime.append(int(string[1]) * 10 + int(string[2]) + 60)
                    count = 60
                if string[0] == '금':
                    tabletime.append(int(string[1]) * 10 + int(string[2]) + 80)
                    count = 80
                if string[0] == '토':
                    tabletime.append(int(string[1]) * 10 + int(string[2]) + 100)
                    count = 100
                    rang = range(0, 6)
            if len(string) == 2:
                if string[0] == '월':
                    tabletime.append(int(string[1]))
                    count = 0
                if string[0] == '화':
                    tabletime.append(int(string[1]) + 20)
                    count = 20
                if string[0] == '수':
                    tabletime.append(int(string[1]) + 40)
                    count = 40
                if string[0] == '목':
                    tabletime.append(int(string[1]) + 60)
                    count = 60
                if string[0] == '금':
                    tabletime.append(int(string[1]) + 80)
                    count = 80
                if string[0] == '토':
                    tabletime.append(int(string[1]) + 100)
                    count = 100
                    rang = range(0, 6)
                if string[0] == '1':
                    tabletime.append(int(string[0]) * 10 + int(string[1]) + count)
            if len(string) == 1:
                tabletime.append(int(string[0]) + count)

    return render(request, 'studyroom.html', {"list": q, "ran": ran, "rang": rang, "room": room_num,
                                    "tabletime": tabletime})


@login_required(login_url='common:login')
def register(request):
    date = request.POST.get("date")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    room_num = request.POST.get("room_num")
    room = int(room_num)
    q = Reserve.objects.filter(room = room_num)
    check = 0
    start_time_i = int(start_time)
    end_time_i = int(end_time)
    time_check = end_time_i - start_time_i
    studytime = []
    tabletime = []
    regtime = []

    if time_check > 3:
        messages.error(request, '한 예약에 3시간을 초과하여 예약하실 수 없습니다.')
        return redirect('index')

    for i in range(start_time_i, end_time_i):
        studytime.append(date+str(i))

    for temp in q:
        temptime = temp.time
        strings = temptime.split(',')
        count = 0

        for string in strings:
            string = string.replace(u'\xa0', u'')
            if len(string) == 3:
                if string[0] == '월':
                    regtime.append(int(string[1]) * 10 + int(string[2]))
                    count = 0
                if string[0] == '화':
                    regtime.append(int(string[1]) * 10 + int(string[2]) + 20)
                    count = 20
                if string[0] == '수':
                    regtime.append(int(string[1]) * 10 + int(string[2]) + 40)
                    count = 40
                if string[0] == '목':
                    regtime.append(int(string[1]) * 10 + int(string[2]) + 60)
                    count = 60
                if string[0] == '금':
                    regtime.append(int(string[1]) * 10 + int(string[2]) + 80)
                    count = 80
                if string[0] == '토':
                    regtime.append(int(string[1]) * 10 + int(string[2]) + 100)
                    count = 100
            if len(string) == 2:
                if string[0] == '월':
                    tabletime.append(int(string[1]))
                    count = 0
                if string[0] == '화':
                    tabletime.append(int(string[1]) + 20)
                    count = 20
                if string[0] == '수':
                    tabletime.append(int(string[1]) + 40)
                    count = 40
                if string[0] == '목':
                    tabletime.append(int(string[1]) + 60)
                    count = 60
                if string[0] == '금':
                    tabletime.append(int(string[1]) + 80)
                    count = 80
                if string[0] == '토':
                    tabletime.append(int(string[1]) + 100)
                    count = 100
            if len(string) == 1:
                tabletime.append(int(string[0]) + count)


    count = 0
    check = 0

    for string in studytime:
        string = string.replace(u'\xa0', u'')
        if len(string) == 3:
            if string[0] == '월':
                regtime.append(int(string[1]) * 10 + int(string[2]))
                count = 0
            if string[0] == '화':
                regtime.append(int(string[1]) * 10 + int(string[2]) + 20)
                count = 20
            if string[0] == '수':
                regtime.append(int(string[1]) * 10 + int(string[2]) + 40)
                count = 40
            if string[0] == '목':
                regtime.append(int(string[1]) * 10 + int(string[2]) + 60)
                count = 60
            if string[0] == '금':
                regtime.append(int(string[1]) * 10 + int(string[2]) + 80)
                count = 80
            if string[0] == '토':
                regtime.append(int(string[1]) * 10 + int(string[2]) + 100)
                count = 100
        if len(string) == 2:
            if string[0] == '월':
                regtime.append(int(string[1]))
                count = 0
            if string[0] == '화':
                regtime.append(int(string[1]) + 20)
                count = 20
            if string[0] == '수':
                regtime.append(int(string[1]) + 40)
                count = 40
            if string[0] == '목':
                regtime.append(int(string[1]) + 60)
                count = 60
            if string[0] == '금':
                regtime.append(int(string[1]) + 80)
                count = 80
            if string[0] == '토':
                regtime.append(int(string[1]) + 100)
                count = 100
            if string[0] == '1':
                regtime.append(int(string[0]) * 10 + int(string[1]) + count)
        if len(string) == 1:
            regtime.append(int(string[0]) + count)

    for b in tabletime:
        if regtime.count(b) != 0:
            check += 1

    if check == 0:
        a = Reserve(author = request.user, time = ','.join(studytime), room = room_num)
        a.save()
        return redirect('studyroom:index', room)
    else:
        messages.error(request, '이미 해당 시간에 예약이 존재합니다.')
        return redirect('studyroom:index', room)


@login_required(login_url='common:login')
def delete(request, class_id):
    reg = get_object_or_404(Reserve, pk=class_id)
    reg.delete()
    return redirect('index')

def delete_everything(request):
    Reserve.objects.all().delete()
