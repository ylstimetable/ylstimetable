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
    floor = request.POST.get("floor") # 학년
    smoke = request.POST.get("smoke") # 흡연여부

    q = Receipt.objects.filter(semester='2024-1')
    for obj in q:
        q_obj = obj

    if request.user in q_obj.voter.all():
        stored_user = Receipt_Student.objects.get(author=request.user)
        temp_error_message = '이미 접수된 사용자입니다. 학년: {}; 흡연여부: {}'.format(stored_user.floor, stored_user.smoke)
        messages.error(request, temp_error_message)
        return redirect('libraryseat:index')
    else:
        messages.success(request, '접수 완료되었습니다.')
        q_obj.voter.add(request.user)
        a = Receipt_Student(author=request.user, student_number = request.user.student_number, floor=floor, smoke=smoke)
        a.save()
        return redirect('libraryseat:index')


@login_required(login_url='common:login')
def random(request):
    r_all = Result.objects.all()
    next_semester = '2024-1'

    semester_list = []

    for r in r_all:
        semester_list.append(r.semester)

    if next_semester in semester_list:
        messages.error(request, '이미 랜덤배정이 완료되었습니다.')
        return redirect('libraryseat:index')

    applicant_list = Receipt.objects.filter(semester='2024-1')
    for obj in applicant_list:
        q = obj

    target = []
    first_app = []
    second_app = []
    third_app = []
    all_app = []

    # Fixed Error: 혹시 신청자가 RECEIPT.voters에서 누락되었을 경우를 대비한 코드!
    RSALL = Receipt_Student.objects.all()
    for r_s in RSALL:
        if not r_s.author in q.voter.all():
            q.voter.add(r_s.author)
            print("UPDATED:")
            print(r_s.author.student_name)
            print(r_s.author.student_number)
            print()
    print("Fixing done")
    print()


    # 관리자님께: 이 부분 수정하여 MY_SHUFFLE_METHOD 변수에 난수추첨 방식을 설정해 놓으시면 됩니다! 
    # MY_SHUFFLE_METHOD = 1 로 설정시: 3-2-1학년 순서로 배열되도록 난수추첨
    # MY_SHUFFLE_METHOD = 2 로 설정시: 학년 관계없이 모두 섞어서 난수추첨 
    MY_SHUFFLE_METHOD = 2

    for applicant in q.voter.all():
        b = Receipt_Student.objects.filter(author=applicant)
        for c in b:
            applicant_receipt = c
            
        all_app.append(applicant.student_number)
        if applicant_receipt.floor == "3":
            third_app.append(applicant.student_number)
        elif applicant_receipt.floor == "2": 
            second_app.append(applicant.student_number)
        else:
            first_app.append(applicant.student_number)

    if MY_SHUFFLE_METHOD==1:     
        #3-2-1 순서 배정방식입니다! 
        shuffle(third_app)
        shuffle(second_app)
        shuffle(first_app)
        # 3학년 우선배정
        for app in third_app:
            target.append(app)
        # 2학년 
        for app in second_app:
            target.append(app)
        # 1학년 학년
        for app in first_app:
            target.append(app)
    else: 
        #모든 학년 함께 섞는 배정방식입니다!
        shuffle(all_app)
        for app in all_app:
            target.append(app)
        
    strings = ','.join(target)
    a = Result(semester='2024-1', sequence=strings, sequence_backup=strings)
    a.save()

    return redirect('libraryseat:index')


@login_required(login_url='common:login')
def register(request):
    result = Result.objects.filter(semester='2024-1')
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
    result = Result.objects.filter(semester='2024-1')
    receipt_start = len(Receipt.objects.filter(semester='2024-1'))
    location = 10000
    random_start = 0
    user = request.user

    if user.student_auth == False:
        return render(request, 'unauth.html')

    if len(Result.objects.filter(semester='2024-1')) == 0:
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
    third_a_floor = range(0,21)
    third_a_floor_end = 21
    third_b_floor = range(21, 141)
    third_b_floor_end = 141
    third_floor_end = 147 # 23여름에 144 좌석에서 146 좌석으로 변경!
    fourth_a_floor = range(0, 35)
    fourth_a_floor_end = 35
    fourth_b_floor = range(35, 163)
    fourth_b_floor_end = 163 # 23여름에 144 좌석에서 162 좌석으로 변경!
    fifth_a_floor = range(0,91)
    fifth_a_floor_end = 91

    ran = range(0,60)
    rang = range(1,6)

    for q in q_all:
        seat_name.append(q.author.student_name)
        seat_num.append(int(q.room))

    return render(request, 'libraryseat_status.html', {"seat_num": seat_num, "seat_name": seat_name, 
                                                        #"third_a_floor": third_a_floor, 
                                                        "third_a_floor_end": third_a_floor_end,
                                                        #"third_b_floor": third_b_floor, 
                                                        "third_b_floor_end": third_b_floor_end,
                                                        "third_floor_end": third_floor_end, 
                                                        #"fourth_a_floor": fourth_a_floor, 
                                                        #"fourth_b_floor": fourth_b_floor,
                                                        "fourth_a_floor_end": fourth_a_floor_end, 
                                                        "fourth_b_floor_end": fourth_b_floor_end,
                                                       "fifth_a_floor_end": fifth_a_floor_end, 
                                                       #"fifth_a_floor": fifth_a_floor, 
                                                       "ran": ran, "rang": rang})

@login_required(login_url='common:login')
def seat_register(request, seat_number):
    # 관리자님께: 매학기 흡연 좌석 현황을 이 배열에 업데이트해 주세요.  
    smoking_zone = [134, 135, 136, 137, 138, 139, 140, 1135, 1136, 1139, 1140, 1143, 1144, 1160, 1161, 1162, 10076, 10077, 10078, 10081, 10082, 10083, 10086, 10087, 10088]

    requested_seat = int(seat_number)
    current_queue = Result.objects.filter(semester='2024-1')
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

                
                # 3학년 전용좌석 처리
                if requested_seat < 1000: 
                    if not applicant_receipt.floor == "3":
                        messages.error(request, "선택하신 좌석은 3학년 전용 구역으로 운영되고 있습니다.")
                        return redirect('libraryseat:reserve_status')
                        
                # 1,2학년 전용좌석 처리
                # 관리자님께: 3학년에게 4,5층 좌석 선택을 허용하려면 이 아래 네줄 코드를 주석처리 해주세요
                if requested_seat >= 1000: 
                    if applicant_receipt.floor == "3": 
                        messages.error(request, "현재는 3층 좌석만 3학년에게 배정하고 있습니다.")
                        return redirect('libraryseat:reserve_status')
                
                # 흡연좌석 처리
                if requested_seat in smoking_zone and applicant_receipt.smoke == "비연": 
                    messages.error(request, "선택하신 좌석은 흡연자 좌석으로 운영되고 있습니다. ")
                    return redirect('libraryseat:reserve_status')    
                if requested_seat not in smoking_zone and applicant_receipt.smoke == "흡연": 
                    messages.error(request, "흡연자는 흡연좌석만 예약 가능합니다.")
                    return redirect('libraryseat:reserve_status')

                # 정상적으로 예약처리
                reserve = Reserve(author=request.user, room=requested_seat)
                reserve.save()
                messages.success(request, '예약이 완료되었습니다.')
                return redirect('libraryseat:reserve_status')

                """
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
                        
                """
            else:
                messages.error(request, '이미 예약하셨습니다.')
                return redirect('libraryseat:reserve_status')
    else:
        #print(requested_seat)
        messages.error(request, '현재 예약 순번이 아닙니다.')
        return redirect('libraryseat:reserve_status')

