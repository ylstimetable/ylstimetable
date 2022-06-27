from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import ClassD, ClassM
from django.contrib import messages
from board.models import ClassA

import requests
from bs4 import BeautifulSoup

@login_required(login_url='common:login')
def result(request):
    if request.method == 'POST':
        name = request.POST.get("classname")
        if name == "개발자":
            return redirect('https://www.instagram.com/kkpark09/')
        class_list = ClassD.objects.filter(semester='2022-2')
        classfind = class_list.filter(
            Q(title__icontains=name) |
            Q(professor__icontains=name) |
            Q(number__icontains=name)
        ).distinct

    else:
        return render(request, 'index.html')

    context = {'lists': classfind}
    return render(request, 'result.html', context)

@login_required(login_url='common:login')
def index(request):
    user = request.user

    if user.student_auth == False:
        return render(request, 'unauth.html')

    q_all = user.class_voter.all()
    q = q_all.filter(semester='2022-2')
    m = user.class_author.all()
    ran = range(1, 14)
    rang = range(0, 5)

    tabletime = []
    tablename = []
    tablecolor = []
    tableroom = []
    colorcount = 0
    saturday = 0
    credit = 0

    for temp in q:
        temptime = temp.time
        tempnam = temp.title
        strings = temptime.split(',')
        colorcount += 1
        count = 0

        for string in strings:
            string = string.replace(u'\xa0', u'')
            tempname = tempnam.replace(u'\xa0', u'')
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
                    saturday = 1
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
                    saturday = 1
                    rang = range(0, 6)
                if string[0] == '1':
                    tabletime.append(int(string[0]) * 10 + int(string[1]) + count)
            if len(string) == 1:
                tabletime.append(int(string[0]) + count)

            tablename.append(tempname)
            tablecolor.append(colorcount)
            tableroom.append(temp.room)
            credit += 1


    for temp in m:
        temptime = temp.time
        tempnam = temp.title
        strings = temptime.split(',')
        colorcount += 1
        count = 0

        for string in strings:
            string = string.replace(u'\xa0', u'')
            tempname = tempnam.replace(u'\xa0', u'')
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
                    saturday = 1
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
                    saturday = 1
                    rang = range(0, 6)
                if string[0] == '1':
                    tabletime.append(int(string[0]) * 10 + int(string[1]) + count)
            if len(string) == 1:
                tabletime.append(int(string[0]) + count)

            tablename.append(tempname)
            tablecolor.append(colorcount)
            tableroom.append('')


    return render(request, 'index.html', {"list": q, "listm": m, "ran": ran, "rang": rang, "credit": credit,
                                    "tabletime": tabletime, "tablename": tablename,
                                          "tablecolor": tablecolor, "tableroom": tableroom, "saturday": saturday})


@login_required(login_url='common:login')
def register(request, class_id):
    q_all = request.user.class_voter.all()
    q = q_all.filter(semester='2022-2')

    reg = get_object_or_404(ClassD, pk=class_id)

    tabletime = []
    regtime = []

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

    temtime = reg.time
    temstring = temtime.split(',')
    count = 0
    check = 0

    for string in temstring:
        string = string.replace(u'\xa0', u'')
        if len(string) == 3:
            if string[0] == '월':
                regtime.append(int(string[1])*10 + int(string[2]))
                count = 0
            if string[0] == '화':
                regtime.append(int(string[1])*10 + int(string[2]) + 20)
                count = 20
            if string[0] == '수':
                regtime.append(int(string[1])*10 + int(string[2]) + 40)
                count = 40
            if string[0] == '목':
                regtime.append(int(string[1])*10 + int(string[2]) + 60)
                count = 60
            if string[0] == '금':
                regtime.append(int(string[1])*10 + int(string[2]) + 80)
                count = 80
            if string[0] == '토':
                regtime.append(int(string[1])*10 + int(string[2]) + 100)
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
                regtime.append(int(string[0])*10+int(string[1])+count)
        if len(string) == 1:
            regtime.append(int(string[0]) + count)


    for b in tabletime:
        if regtime.count(b) != 0:
            check += 1

    if check == 0:
        reg.voter.add(request.user)
        reg.save()
        return redirect('index')
    else:
        messages.error(request, '해당 시간에 수강하는 과목이 있습니다.')
        return redirect('index')


@login_required(login_url='common:login')
def delete(request, class_id):
    reg = get_object_or_404(ClassD, pk=class_id)
    reg.voter.remove(request.user)
    return redirect('index')


@login_required(login_url='common:login')
def manual_delete(request, class_id):
    reg = get_object_or_404(ClassM, pk=class_id)
    reg.delete()
    return redirect('index')


@staff_member_required(login_url='common:login')
def addition(request):
    classlist = {"헌법1": 6101, "헌법2": 6102, "헌법소송법": 6103, "행정법": 6104, "민사소송법1": 6204, "민사소송법2": 6210,
                 "계약법1": 6212, "물권법": 6202, "친족상속법": 6209, "계약법2": 6214, "형법2": 6302, "형사소송법": 6303,
                 "유가증권법": 6403, "보험법": 6404, "독점규제법": 6501, "조세법2": 6504, "사회보장법": 6507, "저작권법": 6604,
                 "국제통상법": 6703, "국제거래법": 6712, "법철학": 6802, "회계와국제기준": 6805, "형사정책": 6305,
                 "불법행위법": 6213, "형법1": 6301, "형사증거법": 6304, "상거래법": 6401, "회사법": 6402, "사이버법": 7610,
                 "소비자보호법": 6502, "조세법1": 6503, "민재실": 7906, "지방자치법": 7107, "환경법": 7109, "CITIZENSHIP": 7112,
                 "지적재산권법개론": 7612, "노동법사례연구": 7505, "INT": 7720,
                 "소송대체적분쟁해결": 7209, "형사특별법": 6308, "자본시장과법": 7404, "CORPORATE": 7414, "경통사": 7417,
                 "첨단의료": 7620, "협상워크숍": 7807, "LAW POLITICS": 7811, "상응": 7904, "형재실": 7907, "검실1": 7913,
                 "사실인정론": 7940, "경찰실무": 7943, "법원실무리걸클리닉": 7951, "INTERNATIONAL": 7944, "스타트업": 7958,
                 "젊은예술인": 7961, "집단적노사관계법": 6505, "특허법": 6602, "국제법": 6701, "법사회학": 6804, "서양법제사": 6803,
                 "법정보": 6901, "법조윤리": 6902, "법문서작성": 6903, "모의재판": 6904, "법사상사": 6801, "배심제": 7304,
                 "실무수습": 6905, "행통사": 7114, "헌통사": 7115, "민통사": 7205, "민소사": 7210, "상통사": 7416,
                 "법인세법": 7503, "생명윤리법": 7601, "문화산업법": 7608, "한국법제사": 7803, "민응": 7902, "공쟁실": 7905,
                 "공익소송리걸클리닉": 7925, "사회적기업청년창업법률지원리걸클리닉": 7937, "기업인수합병의이론과실무": 7938,
                 "사회배려자법률지원리걸클리닉": 7953, "형법작": 7956,  "민사리걸클리닉": 7959, "검찰실무2": 7957,
                 "행정구제법": 6106, "채권담보권": 6205, "민사집행법": 6211, "물권법판례연습": 6215, "개별적근로관계법": 6506,
                 "상표법": 6603, "요건사실론": 7211, "스포츠엔터": 7609, "법의학": 7621,
                 "국제환경법": 7705, "국제분쟁해결제도": 6714, "지역주민": 7936, "주요대법원": 7962, "형통사": 6307,
                 "손해배상법": 6208, "AMERICAN LAW": 6706, "LAW AND POLITICS": 6815, "도산법": 7403, }

    assess = ClassA.objects.all()

    user = request.user

    if user.student_auth == False:
        return render(request, 'unauth.html')

    if request.method == 'POST':
        for name in classlist:
            control = 0
            classnum = classlist[name]
            for i in range(1, 7):
                url = f"http://ysweb.yonsei.ac.kr:8888/curri120601/curri_pop2.jsp?&hakno=YJD{classnum}&bb=0{i}&sbb=00&domain=W&startyy=2022&hakgi=2&ohak=23100"
                req = requests.get(url)
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')

                if soup.select_one('body > form > table:nth-child(3) > tr:nth-child(3) > td:nth-child(2)') is None:
                    break;

                temptitle = soup.select_one(
                    'body > form > table:nth-child(3) > tr:nth-child(3) > td:nth-child(2)').string

                temproom = soup.select_one(
                    'body > form > table:nth-child(3) > tr:nth-child(4) > td:nth-child(2)').string

                tempprof = soup.select_one(
                    'body > form > table:nth-child(3) > tr:nth-child(6) > td:nth-child(2)').string

                temptime = soup.select_one(
                    'body > form > table:nth-child(3) > tr:nth-child(4) > td:nth-child(4)').string

                strings = temptime.split(',')
                tabletime = []
                count = 0

                for string in strings:
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

                t = ClassD(title=temptitle, room=temproom, professor=tempprof, time=temptime,
                              semester='2022-2', number=f"YJD{classnum}", ban=i)
                t.save()

                for asses in assess:
                    if temptitle == asses.subject:
                        if tempprof == asses.professor:
                            sem = asses.semester
                            asses.semester = f"2022-2, {sem}"
                            control = 1
                            asses.save()

                if control == 0:
                    a = ClassA(subject=temptitle, professor=tempprof, semester = '2022-2', rate = '0')
                    a.save()

    return render(request, 'addition.html')


@login_required(login_url='common:login')
def address(request, number, ban):
    addr = f"http://ysweb.yonsei.ac.kr:8888/curri120601/curri_pop2.jsp?&hakno={number}&bb=0{ban}&sbb=00&domain=W&startyy=2022&hakgi=2&ohak=23100"
    return redirect(addr)

@login_required(login_url='common:login')
def privacy(request):
    return render(request, 'privacy.html')

@login_required(login_url='common:login')
def contract(request):
    return render(request, 'contract.html')


@login_required(login_url='common:login')
def manual_register(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        time = request.POST.get("time")
    else:
        return render(request, 'index.html')

    q = request.user.class_voter.all()
    m = request.user.class_author.all()
    reg = ClassM(title=title, time=time)

    tabletime = []
    regtime = []

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

    for temp in m:
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

    temtime = reg.time
    temstring = temtime.split(',')
    count = 0
    check = 0

    for string in temstring:
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
        reg.save()
        reg.author.add(request.user)
        return redirect('index')
    else:
        messages.error(request, '해당 시간에 수강하는 과목이 있습니다.')
        return redirect('index')

