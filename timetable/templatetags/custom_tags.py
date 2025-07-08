from django import template
import datetime
from libraryseat.models import Receipt

register = template.Library()

@register.simple_tag
def add_str(left, right):
    return left + right*20

@register.simple_tag
def change(value):
    if value == True:
        a = 'O'
        return a
    else:
        a = 'X'
        return a

@register.simple_tag
def pull(list):
    list.reverse()
    value = list.pop()
    return value

@register.simple_tag
def seatnum_cal(i, j):
    value = int(i*5+j)
    return value

@register.simple_tag
def location(list, loc):
    a = list.index(loc)
    return a

@register.simple_tag
def location_plus(list, loc):
    a = list.index(loc)+1
    return a

@register.simple_tag
def next(list, num):
    a = list[num]
    return a

@register.simple_tag
def date(num):
    if num == 0:
        date = "월"
        return date
    elif num == 1:
        date = "화"
        return date
    elif num == 2:
        date = "수"
        return date
    elif num == 3:
        date = "목"
        return date
    elif num == 4:
        date = "금"
        return date
    elif num == 5:
        date = "토"
        return date
    elif num == 6:
        date = "일"
        return date

@register.simple_tag
def content(list, loc):
    a = list[loc]
    return a

@register.simple_tag
def time(ctime):
    ptime = int(ctime)+8
    return ptime

@register.filter
def sub(value, arg):
    return value -arg

@register.simple_tag
def subst(value):
    value -= 1
    return value

@register.simple_tag
def divide(value):
    value = value % 10
    return value

@register.simple_tag
def num(value):
    value = float(value)
    value = round(value, 2)
    return value

@register.simple_tag
def date_start(value):
    receipt = Receipt.objects.filter(semester='2025-2')
    for re in receipt:
        receipt = re
    day_standard = datetime.datetime(2025, int(receipt.month), int(receipt.day), 0, 0, 0)
    diff_hours = datetime.timedelta(hours=9)
    diff_minutes = datetime.timedelta(minutes=5)
    diff_days = datetime.timedelta(days=1)
    if int(value) < 168:
        reserve_time = day_standard + diff_minutes*int(value) + diff_hours
    elif int(value) >= 168 and int(value) < 336:
        reserve_time = day_standard + diff_days + diff_minutes * (int(value) - 168) + diff_hours
    else:
        reserve_time = day_standard + diff_days + diff_days + diff_minutes*(int(value)-336) + diff_hours

    return reserve_time

@register.simple_tag
def date_ten_minutes(value):
    receipt = Receipt.objects.filter(semester='2025-2')
    for re in receipt:
        receipt = re
    day_standard = datetime.datetime(2025, int(receipt.month), int(receipt.day), 0, 0, 0)
    diff_hours = datetime.timedelta(hours=9)
    diff_minutes = datetime.timedelta(minutes=5)
    diff_days = datetime.timedelta(days=1)
    if int(value) < 168:
        reserve_time = day_standard + diff_minutes*(int(value)+1) + diff_hours
    elif int(value) >= 168 and int(value) < 336:
        reserve_time = day_standard + diff_days + diff_minutes*(int(value)-167) + diff_hours
    else:
        reserve_time = day_standard + diff_days + diff_days + diff_minutes*(int(value)-335) + diff_hours

    return reserve_time

@register.simple_tag
def start_time(list):

    string = list.split(',')
    ptime = int(string[0]) + 8

    return ptime

@register.simple_tag
def compare_time(current_time):
    if current_time.weekday() == 0:
        if current_time.hour < 8:
            return False
        else:
            return True
    else:
        return True

@register.simple_tag
def end_time(list):
    string = list.split(',')
    if len(string) == 1:
        end_time = int(string.pop()) + 9
        return end_time
    else:
        end_time = int(string.pop()) + 9
        return end_time

@register.simple_tag
def fourth(num):
    num = num+1000
    return num

@register.simple_tag
def fifth(num):
    num = num+10000
    return num

@register.simple_tag
def room(num):
    a = int(num)
    if a == 1:
        b = "B126"
        return b
    elif a == 2:
        b = "B127"
        return b
    elif a == 3:
        b = "B112"
        return b
    elif a == 4:
        b = "B113"
        return b
    elif a == 5:
        b = "B114"
        return b
    elif a == 6:
        b = "B116"
        return b
    elif a == 7:
        b = "212C"
        return b
    elif a == 8:
        b = "212D"
        return b
    elif a == 9:
        b = "212E"
        return b
    elif a == 10:
        b = "212F"
        return b
