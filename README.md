# YLS Timetable 개발매뉴얼

## Quick Start Guide

### Setting up dev environment

(리눅스 기준으로 서술하고있습니다... 이런 나라서 미안해)

#### Creating tables locally
```
 $ python manage.py makemigrations --settings=timetabl.settings.local
 $ python manage.py migrate --run-syncdb --settings=timetabl.settings.local
```

#### Creating and authenticating yourself as a superuser
```
 $ python manage.py createsuperuser --settings=timetabl.settings.local
 $ python manage.py runserver --settings=timetabl.settings.loc
```

And then...

1. Go to http://127.0.0.1:8000/adminlee 
1. Sign in to give yourself credentials

로컬서버를 종료하지 않은 채로 쭉 작업하시면 됩니다. 

### Shipping prod code
1. Lightsail 로그인 하자! 브라우저에서 ssh into the virtual machine!
1. ``` $ cd venvs/mysite/bin```
1. ``` $ . activate```
1. ``` $ cd ~/projects/mysite```
1. ``` $ git pull <Whatever you need to pull>```
1. ``` $ sudo systemctl restart mysite.service```

만일 Application을 새로 만들어 추가한 경우 아래의 작업도 추가적으로 해주세요. 
1. ``` $ python manage.py makemigrations <application name> --settings=timetabl.settings.local```
1. ``` $ python manage.py migrate --run-syncdb <application name> --settings=timetabl.settings.local```

## Maintenance Guide  

### 설문조사 기능

admin 페이지에서 post 새로 작성할 때에 유의할 점! 
1. 질문제목은 띄어쓰기 없이 한 단어로, 내용은 그냥 줄글로 쓰면 되고 선택지는 쉼표로 구분하여 한줄로 쓸것 (e.g. 흡연, 비흡연, 무응답)
1. 파싱 과정에서 문제 생길수있으니 선택지 본문에 쉼표 (,) 는 사용하지 말것! 
1. 현재 설문 마감일자를 월과 일로만 입력받고 있습니다. 코드 수정이 있을때까지는 해를 넘기는 설문은 만들지 말아주세요 ㅜㅜ

### 열람실 좌석배정 시즌
1. 흡연좌석 현황 업데이트!

### 수강신청 시즌

## Tips and Discussions
