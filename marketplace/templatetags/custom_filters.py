from django import template

register = template.Library()


@register.filter(name="half")
def half_string(value: str):
    n = value.split(".")
    return n[0]


@register.filter(name="timesrange")
def times(number):
    return range(5)
