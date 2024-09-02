from django import template
from math import ceil, floor


register = template.Library()


@register.filter
def floor_500(price):
    return floor(int(price)/500) * 500


@register.filter
def ceil_500(price):
    return ceil(int(price)/500) * 500
