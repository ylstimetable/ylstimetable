from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Receipt, Reserve, Result, Receipt_Student
from random import shuffle
import datetime

@login_required(login_url='common:login')
def create_receive(request):
    sem = request.POST.get("semester")
    month = request.POST.get("month")
    day = request.POST.get("day")
    q_count = len(Receipt.objects.filter(semester=sem))

    if q_count != 0:
        messages.error(request, "해당 학기의 좌석배정 로그가 이미 존재합니다.")
        return redirect('libraryseat:index')
    else:
        a = Receipt(semester=sem, month=month, day=day)
        a.save()
        return redirect('libraryseat:index')


@staff_member_required(login_url='common:login')
def seat_admin(request):
    return render(request, 'libraryseat_admin.html')

@login_required(login_url='common:login')
def floor(request):
    return render(request, 'floor.html')

@login_required(login_url='common:login')
def receive(request):
    floor = request.POST.get("floor")
    student_fee = request.POST.get("student_fee")
    smoke = request.POST.get("smoke")

    q = Receipt.objects.filter(semester='2022-2')
    for obj in q:
        q_obj = obj

    if request.user in q_obj.voter.all():
        messages.error(request, '이미 접수된 사용자입니다.')
        return redirect('libraryseat:index')
    else:
        messages.success(request, '접수 완료되었습니다.')
        q_obj.voter.add(request.user)
        a = Receipt_Student(author=request.user, fee=student_fee, floor=floor, smoke=smoke)
        a.save()
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

    target = []
    fee_app = []
    non_fee_app = []

    for applicant in q.voter.all():
        b = Receipt_Student.objects.filter(author=applicant)
        for c in b:
            applicant_receipt = c

        if applicant_receipt.fee == "납부":
            fee_app.append(applicant.student_number)
        else:
            non_fee_app.append(applicant.student_number)

    shuffle(fee_app)
    shuffle(non_fee_app)

    for app in fee_app:
        target.append(app)

    for app in non_fee_app:
        target.append(app)

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
    user = request.user

    if user.student_auth == False:
        return render(request, 'unauth.html')

    if len(Result.objects.filter(semester='2022-2')) == 0:
        return render(request, 'libraryseat.html', {'location': location,
                                                    'random_start': random_start, 'receipt_start': receipt_start})
    else:
        for re in result:
            result = re
        list = result.sequence_backup.split(',')
        random_start = 1

        if request.user.student_number in list:
            location = list.index(request.user.student_number)

        return render(request, 'libraryseat.html', {'location': location, 'list': list,
                                                    'random_start': random_start, 'receipt_start': receipt_start})

@login_required(login_url='common:login')
def reserve_status(request):
    q_all = Reserve.objects.all()

    seat_num = []
    seat_name = []
    third_floor = range(0,129)
    third_floor_end = 130
    third_smoke_start = 72
    third_smoke_end = 85
    fourth_ga_floor = range(0, 60)
    fourth_ga_floor_end = 61
    fourth_na_floor = range(61,152)
    fourth_na_floor_end = 153
    fourth_smoke_start = 98
    fourth_smoke_end = 111
    fifth_a_floor = range(0,62)
    fifth_a_floor_end = 62
    fifth_b_floor = range(62,119)
    fifth_b_floor_end = 120
    ran = range(0,60)
    rang = range(1,6)

    for q in q_all:
        seat_name.append(q.author.student_name)
        seat_num.append(int(q.room))


    return render(request, 'libraryseat_status.html', {"seat_num": seat_num, "seat_name": seat_name, "third_floor": third_floor, "third_floor_end": third_floor_end,
                                                       "third_smoke_start": third_smoke_start, "third_smoke_end": third_smoke_end,
                                                       "fourth_ga_floor_end": fourth_ga_floor_end, "fourth_na_floor_end": fourth_na_floor_end,
                                                       "fourth_smoke_start": fourth_smoke_start, "fourth_smoke_end": fourth_smoke_end,
                                                       "fifth_a_floor_end": fifth_a_floor_end, "fifth_b_floor_end": fifth_b_floor_end,
                                                       "fourth_ga_floor": fourth_ga_floor, "fourth_na_floor": fourth_na_floor,
                                                       "fifth_a_floor": fifth_a_floor, "fifth_b_floor": fifth_b_floor, "ran": ran, "rang": rang})

@login_required(login_url='common:login')
def seat_register(request, seat_number):
    requested_seat = int(seat_number)
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
            already_reserve = len(Reserve.objects.filter(author=request.user))
            if already_reserve == 0:
                b = Receipt_Student.objects.filter(author=request.user)
                for c in b:
                    applicant_receipt = c

                if applicant_receipt.smoke == "흡연":
                    if 72 > requested_seat > 84 or 1098 > requested_seat > 1111:
                        messages.error(request, "흡연자는 흡연좌석만 예약 가능합니다.")
                        return redirect('libraryseat:index')

                if applicant_receipt.floor == "3층":
                    if requested_seat < 1000:
                        if applicant_receipt.smoke == "흡연":
                            if requested_seat < 73 or requested_seat > 84:
                                messages.error(request, "흡연자는 흡연좌석만 예약 가능합니다.")
                                return redirect('libraryseat:reserve_status')
                        reserve = Reserve(author=request.user, room=requested_seat)
                        reserve.save()
                        messages.success(request, '예약이 완료되었습니다.')
                        return redirect('libraryseat:reserve_status')
                    else:
                        messages.error(request, "3층 신청자는 3층 구역만 예약하실 수 있습니다.")
                        return redirect('libraryseat:reserve_status')

                if applicant_receipt.floor == "4층":
                    if 999 < requested_seat < 2000:
                        if applicant_receipt.smoke == "흡연":
                            if requested_seat < 1099 or requested_seat > 1110:
                                messages.error(request, "흡연자는 흡연좌석만 예약 가능합니다.")
                                return redirect('libraryseat:reserve_status')
                        reserve = Reserve(author=request.user, room=requested_seat)
                        reserve.save()
                        messages.success(request, '예약이 완료되었습니다.')
                        return redirect('libraryseat:reserve_status')
                    else:
                        messages.error(request, "4층 신청자는 4층 구역만 예약하실 수 있습니다.")
                        return redirect('libraryseat:reserve_status')

                if applicant_receipt.floor == "5층":
                    if 9999 < requested_seat:
                        reserve = Reserve(author=request.user, room=requested_seat)
                        reserve.save()
                        messages.success(request, '예약이 완료되었습니다.')
                        return redirect('libraryseat:reserve_status')
                    else:
                        messages.error(request, "5층 신청자는 5층 구역만 예약하실 수 있습니다.")
                        return redirect('libraryseat:reserve_status')
            else:
                messages.error(request, '이미 예약하셨습니다.')
                return redirect('libraryseat:reserve_status')
    else:
        messages.error(request, '현재 예약 순번이 아닙니다.')
        return redirect('libraryseat:reserve_status')

