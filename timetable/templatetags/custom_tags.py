from django import template

register = template.Library()

@register.simple_tag
def add_str(left, right):
    return left + right*20

@register.simple_tag
def location(list, loc):
    a = list.index(loc)
    return a

@register.simple_tag
def content(list, loc):
    a = list[loc]
    return a

@register.simple_tag
def time(ctime):
    ptime = ctime+8
    qtime = ptime % 12
    if qtime == 0:
        qtime += 12
    return qtime

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