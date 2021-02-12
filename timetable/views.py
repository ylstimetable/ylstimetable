from django.shortcuts import render, get_object_or_404, redirect
from .form import ClassForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import ClassD
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse


import requests
from bs4 import BeautifulSoup

@login_required(login_url='common:login')
def result(request):
    if request.method == 'POST':
        name = request.POST.get("classname")
        class_list = ClassD.objects.all()
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
    q = user.class_voter.all()
    ran = range(1, 13)
    rang = range(0, 5)

    tabletime = []
    tablename = []
    tablecolor = []
    tableroom = []
    colorcount = 0

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
                if string[0] == '1':
                    tabletime.append(int(string[0]) * 10 + int(string[1]) + count)
            if len(string) == 1:
                tabletime.append(int(string[0]) + count)

            tablename.append(tempname)
            tablecolor.append(colorcount)
            tableroom.append(temp.room)

    return render(request, 'index.html', {"list": q, "ran": ran, "rang": rang,
                                    "tabletime": tabletime, "tablename": tablename,
                                          "tablecolor": tablecolor, "tableroom": tableroom})


@login_required(login_url='common:login')
def register(request, class_id):
    q = request.user.class_voter.all()

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


def addition(request):
    classlist = {"헌법": 6101, "행정법": 6104, "민사소송법": 6210, "계약법": 6212,
                 "불법행위법": 6213, "형법": 6301, "형사증거법": 6304, "상거래법": 6401, "회사법": 6402,
                 "소비자보호법": 6502, "조세법": 6503, "민재실": 7906,
                 "집단적노사관계법": 6505, "특허법": 6602, "국제법": 6701, "법사회학": 6804, "서양법제사": 6803,
                 "법정보": 6901, "법조윤리": 6902, "법문서작성": 6903, "모의재판": 6904,
                 "실무수습": 6905, "행통사": 7114, "헌통사": 7115, "민통사": 7205, "민소사": 7210, "상통사": 7416,
                 "법인세법": 7503, "생명윤리법": 7601, "문화산업법": 7608, "한국법제사": 7803, "민응": 7902, "공쟁실": 7905,
                 "공익소송리걸클리닉": 7925, "사회적기업청년창업법률지원리걸클리닉": 7937, "기업인수합병의이론과실무": 7938,
                 "사회배려자법률지원리걸클리닉": 7953, "형법작": 7956, "검찰실무": 7957, "민사리걸클리닉": 7959}

    if request.method == 'POST':
        name = request.POST.get("classname")
        if name in classlist:
            classnum = classlist[name]
            for i in range(1, 5):
                url = f"http://ysweb.yonsei.ac.kr:8888/curri120601/curri_pop2.jsp?&hakno=YJD{classnum}&bb=0{i}&sbb=00&domain=W&startyy=2021&hakgi=1&ohak=23100"
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
                              semester='2021-2', number=f"YJD{classnum}", ban=i)
                t.save()

    return render(request, 'addition.html')

@login_required(login_url='common:login')
def address(request, number, ban):
    addr = f"http://ysweb.yonsei.ac.kr:8888/curri120601/curri_pop2.jsp?&hakno={number}&bb=0{ban}&sbb=00&domain=W&startyy=2021&hakgi=1&ohak=23100"
    return redirect(addr)
