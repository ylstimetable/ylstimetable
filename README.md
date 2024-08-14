# YLS Timetable 개발매뉴얼

## 기본 관리 매뉴얼 
### User View와 Admin View
[![튜토리얼 비디오](https://img.youtube.com/vi/AJySSrQF6jA/0.jpg)](https://youtu.be/AJySSrQF6jA)
* 이미지를 클릭하면 튜토리얼 비디오로 연결됩니다 

## Quick Start Guide

### Setting up dev environment

(리눅스 기준으로 서술하고있습니다... 이런 나라서 미안해)

#### Cloning git repo
이 Repository의 내용물을 로컬머신에 내려받아주세요~! (나는 git practice의 표준을 잘 모르니까 각자 알아서 git 잘 쓰기)

#### Creating tables locally
```
 $ python manage.py makemigrations --settings=timetabl.settings.local
 $ python manage.py migrate --run-syncdb --settings=timetabl.settings.local
```

#### Creating and authenticating yourself as a superuser
```
 $ python manage.py createsuperuser --settings=timetabl.settings.local
 $ python manage.py runserver --settings=timetabl.settings.local
```

And then...

1. Go to http://127.0.0.1:8000/adminlee 
1. Sign in to give yourself credentials

로컬서버를 종료하지 않은 채로 쭉 작업하시면 됩니다. 

### Shipping prod code

[Lightsail](https://lightsail.aws.amazon.com/) 계정정보
*  아이디 : 개별적으로 전달
* 비밀번호 : 개별적으로 전달

1. Lightsail 로그인 하자! Ubuntu-1 누른 뒤에 "ssh 로 연결" 버튼 누르기
1. 검은 창에 아래의 명령어들을 순차적으로 복사 붙여넣기
1. ``` $ cd venvs/mysite/bin```
1. ``` $ . activate```
1. ``` $ cd ~/projects/mysite```
1. ``` $ git pull <Whatever you need to pull>```
1. ``` $ sudo systemctl restart mysite.service```

만일 Application을 새로 만들어 추가한 경우 아래의 작업도 추가적으로 해주세요. 
1. ``` $ python manage.py makemigrations <application name> --settings=timetabl.settings.prod```
1. ``` $ python manage.py migrate --run-syncdb <application name> --settings=timetabl.settings.prod```

## Maintenance Guide  

### 설문조사 기능

admin 페이지에서 post 새로 작성할 때에 유의할 점! 
1. 질문제목은 띄어쓰기 없이 한 단어로, 내용은 그냥 줄글로 쓰면 되고 선택지는 쉼표로 구분하여 한줄로 쓸것 (e.g. 흡연, 비흡연, 무응답)
1. 파싱 과정에서 문제 생길수있으니 선택지 본문에 쉼표 (,) 는 사용하지 말것! 
1. 현재 설문 마감일자를 월과 일로만 입력받고 있습니다. 코드 수정이 있을때까지는 해를 넘기는 설문은 만들지 말아주세요 ㅜㅜ

### 열람실 좌석배정 시즌
#### 신청 전에 YTT 관리자가 해야 할 일 
1. 권한: 깃헙리포 권한은 11기 이환 변호사님께, YTT 관리자계정 승인은 전대 YTT 관리자에게 받기~!
1. 코드수정: libraryseat/cron.py 에 2023->해당년도로, 2023-1->해당학기로 수정
1. 코드수정: libraryseat/view.py 에 2023-1->해당학기로 수정
1. 코드수정: timetable/templatetags/custom_tags.py 2023->해당년도로, 2023-1->해당학기로 수정
1. 코드수정: templates/libraryseat.html 이런거에도 표기 수정은 간단하게 해주세요!
1. admin 페이지: Reserve 오브젝트들중에 사용x 좌석 네개만 남기고 삭제하기 (10044, 10045, 10089, 10090)
1. admin 페이지: Receipt-student 오브젝트도 전부 삭제해버리기
1. admin 페이지: 우선배정 받은 사람들 좌석번호와 매칭해서 Reserve object로 추가해두기
1. 서버: 업데이트된 모든 코드들 git pull 하기 
1. 서버: cron 잘 돌아가고 있는지 확인 
1. 테스트: EC2미니서버로 시뮬레이션 돌려보기!
1. admin 페이지: 신청서 오픈준비가 다 되면 Receipt 해당학기와 본배정 시작일 넣어서 생성
1. 공지: 접수신청기간 및 배정방법 카톡공지 및 카페공지로 날리기

##### Cron 잘 돌아가고있는지 확인하는 법 
```
 $ python manage.py crontab show --settings=timetabl.settings.prod
```

##### EC2 미니서버로 시뮬레이션 돌리는 법
몰라.. 나중에 시간 되면 더 자세히 적을게... 2023년 1학기 기준으로 10불정도 나왔당. 저는 그냥 개인적으로 지출했는데 내년부터는 총무랑 의논해서 비용처리 하세요.
1. EC2 instance를 만든다. ubuntu micro면 차고 넘침. 
1. 8000번 포트 0.0.0.0/0 에 열어주는 inbound rule 더해주기. 
1. Elastic IP (탄력적 IP) 받아서 EC2 인스턴스에 연결해주기. 
1. 리포에서 코드 받아오기
1. timetabl/settings/base.py 들어가서 allowed_hosts랑 이것저것 수정해주기 (이것저것이 뭐냐고는 나한테 묻지마세요..)
1. 서버에 서비스 업데이트 할 때처럼 migrate하고 run 하자!
1. 이제 탄력적 IP 사용해서 00.000.00.00:8000 에 들어가면 ylstimetable과 똑같은 환경에서 실험할 수 있음. 
1. IT팀원들 및 국장들한테 아이디 열개씩 만들어달라고 부탁. 학년별로 정해진 학번과 이메일 주소 scheme 만들어두는것을 추천. 
1. 시뮬레이션 돌려돌려! 

[좀더 자세한 매뉴얼](https://docs.google.com/document/d/1NyVns_pI_mAHi7PvhE0YL5rzzR9AMnsDbmn8mF4JKTw/edit?usp=sharing)

[잘 모르겠으면 이 링크 참조하세요](https://velog.io/@dojun527/AWS-EC2-Django-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0)

#### 신청 후에 YTT 관리자가 해야 할 일 
1. 난수추첨은 http://ylstimetable.com/libraryseat/admin/ 들어가서 학기-본배정월-본배정일 넣고 생성 누르면 됨! 이거 누르면 다른 사람들도 바로 추첨결과 볼 수 있으니까 신중하게 할것! 녹화할것!
1. 흡연좌석 결정 후 좌석표 수정해서 사진에 업데이트 하기
   사진 업데이트는 ylstimetable/static/images/ (https://github.com/ylstimetable/ylstimetable/tree/master/static/images)
   사진 2개씩 해서 3층은 third_floor, IMG_0811/ 4층은 fourth_floor, IMG_0812, / 5층은 fifth_floor, IMG_0813 (왜 2개씩인지는 나도 모르니 그냥 따라하길,,)
   기존에 있던 파일 지우고 새롭게 캡쳐하고 이름은 윗줄처럼 해서 올리면 됨.

1. 당일 아홉시쯤 일어나서 한 30분쯤 오류없게 대기하기.. 
1. 배정 중간에 코드 업데이트 필요하면 당사자에게 연락해서 수동으로 자리 등록해주고 5분안에 빠르게 업데이트!

##### 수동으로 자리 등록해주는 법
1. http://ylstimetable.com/adminlee/libraryseat/reserve/ 들어가기
1. Reserve 추가
1. 신청하는 사람 이메일 선택하고 좌석번호 적어주기 (3층은 좌석표상의 번호 그대로, 4층은 1000+좌석표번호, 5층은 10000+좌석표번호)

### 수강신청 시즌

#### 코드 업데이트
1. 우선 timetable/views.py에서 '2023-2' 이런 형식으로 되어있는것 전부 해당학기로 바꿔주세요!
2. templates/index.html 여기서도 2024-2학기 바꾸기!
1. 2023년 포털개편 이후 수강편람 크롤링이 어려워져서 수업 시간표등은 우선 수동으로 업데이트 하였습니다... 너넨 이런거 하지 마라 (후)

## Tips and Discussions
