from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Reserve
import datetime


@login_required(login_url='common:login')
def index(request, room_num):

    user = request.user
    if user.student_auth == False:
        return render(request, 'unauth.html')

    my_reserve = Reserve.objects.filter(author = request.user)
    ran = range(1, 15)
    rang = range(0, 7)
    count = 0
    tabletime = []
    daytable = []

    temp_today = datetime.datetime.now()
    if temp_today.weekday() != 0:
        temporary = temp_today - datetime.timedelta(days=int(temp_today.weekday()))
    else:
        if temp_today.hour < 8:
            temporary = temp_today - datetime.timedelta(days=7)
        else:
            temporary = temp_today - datetime.timedelta(days=int(temp_today.weekday()))

    day_standard = temporary
    temp = temporary
    diff_days = datetime.timedelta(days=1)
    daytable.append(day_standard)

    for i in range(0, 6):
        temp = temp + diff_days
        daytable.append(temp)

    for table_date in daytable:
        table_date_reserve = Reserve.objects.filter(year = table_date.year, month = table_date.month,
                                                    day = table_date.day, room = room_num)

        for reserve in table_date_reserve:
            temptime = reserve.time
            strings = temptime.split(',')
            for string in strings:

                tabletime.append(int(string)+count)

        count = count+20


    return render(request, 'studyroom.html', {"ran": ran, "rang": rang, "room": room_num, "current_time": datetime.datetime.now(),
                                    "tabletime": tabletime, "daytable": daytable, "my_reserve": my_reserve})


@login_required(login_url='common:login')
def register(request):
    date = request.POST.get("date")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    room_num = request.POST.get("room_num")
    room = int(room_num)

    temp_today = datetime.datetime.now()
    if temp_today.weekday() != 0:
        temp = temp_today - datetime.timedelta(days=int(temp_today.weekday()))
    else:
        if temp_today.hour < 8:
            temp = temp_today - datetime.timedelta(days=7)
        else:
            temp = temp_today - datetime.timedelta(days=int(temp_today.weekday()))

    delta_date = int(date)
    object_date = temp + datetime.timedelta(days=delta_date)
    q = Reserve.objects.filter(room = room_num)
    already_reserve = Reserve.objects.filter(author=request.user)
    check = 0
    total_time = 0
    max_day_time = 0
    start_time_i = int(start_time)
    end_time_i = int(end_time)
    time_check = end_time_i - start_time_i
    studytime = []

    for reserve in already_reserve:
        if object_date.year == int(reserve.year):
            if object_date.month == int(reserve.month):
                if object_date.day == int(reserve.day):
                    day_reserve_string = reserve.time.split(',')
                    max_day_time = max_day_time + len(day_reserve_string)

    max_day_time = max_day_time + time_check

    if max_day_time > 4:
        messages.error(request, '하루에 예약 가능한 시간은 최대 4시간입니다.')
        return redirect('studyroom:index', room)

    if time_check < 1:
        messages.error(request, '잘못된 시간 선택입니다.')
        return redirect('studyroom:index', room)

    for i in range(start_time_i, end_time_i):
        studytime.append(str(i))

    for reserve in already_reserve:
        reserve_string = reserve.time.split(',')
        total_time = total_time + len(reserve_string)

    total_time = total_time + time_check

    if total_time > 8:
        messages.error(request, '한 주에 예약하실 수 있는 최대 시간은 8시간입니다.')
        return redirect('studyroom:index', room)

    for temp in q:
        if int(temp.year) == object_date.year:
            if int(temp.month) == object_date.month:
                if int(temp.day) == object_date.day:
                    temptime = temp.time
                    strings = temptime.split(',')
                    for b in strings:
                        if studytime.count(b) != 0:
                            check += 1

    if check == 0:
        a = Reserve(author = request.user, time = ','.join(studytime), year = object_date.year, month = object_date.month,
                    day = object_date.day, date = object_date.weekday(), room = room_num)
        a.save()
        messages.success(request, '예약이 완료되었습니다.')
        return redirect('studyroom:index', room)
    else:
        messages.error(request, '이미 해당 시간에 예약이 존재합니다.')
        return redirect('studyroom:index', room)


@login_required(login_url='common:login')
def delete(request, reserve_id):
    reg = get_object_or_404(Reserve, pk=reserve_id)
    reg_time_strings = reg.time.split(',')
    last_time = int(reg_time_strings.pop()) + 9
    reserve_time = datetime.datetime(int(reg.year), int(reg.month), int(reg.day), last_time, 0, 0)
    time_now = datetime.datetime.now()
    room = reg.room

    if time_now > reserve_time:
        messages.error(request, '시간 도과된 예약은 취소할 수 없습니다.')
        return redirect('studyroom:index', room)

    reg.delete()
    return redirect('studyroom:index', room)

