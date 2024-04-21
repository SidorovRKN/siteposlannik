from django import template

register = template.Library()


@register.filter
def intpart(value):
    return int(value)


@register.filter
def decpart(value):
    return int((value % 1) * 100)