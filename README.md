# YLS Timetable 개발매뉴얼

## Quick Start Guide

### Setting up Miniconda environment


#### Creating tables locally
```
python manage.py makemigrations --settings=timetabl.settings.local
python manage.py migrate --run-syncdb --settings=timetabl.settings.local
```

#### Creating and authenticating yourself as a superuser
```
python manage.py createsuperuser --settings=timetabl.settings.local
```
And then...

1. http://127.0.0.1:8000 and sign in
1. http://127.0.0.1:8000/adminlee and give yourself credentials


### Trying running on dev mod

```python manage.py runserver --settings=timetabl.settings.local```


## Maintenance Guide  

### 열람실 좌석배정 시즌

### 수강신청 시즌

## Tips and Discussions
