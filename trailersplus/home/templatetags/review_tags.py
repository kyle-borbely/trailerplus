from django import template
from math import floor, ceil
from trailersplus.utils.objects import get_time_ago


register = template.Library()


@register.filter()
def stars_generator(rating):
    if rating is None:
        rating = 0
    full_stars = floor(rating)
    decimal = int((rating-full_stars)*100)
    empty_stars = 5 - ceil(rating)
    for _ in range(full_stars):
        yield "100%"
    if bool(decimal):
        yield f"{decimal}%"
    for _ in range(empty_stars):
        yield "0"


@register.filter
def star_range(number, minus=None):
    if minus is not None:
        yield from range((minus - number))
    else:
        yield from range(number)


@register.filter
def ago(d1):
    return get_time_ago(d1)


@register.filter
def shortener(content):
    if len(content) > 100:
        return content[:96] + "..."
    return content


@register.filter
def header(content):
    if len(content) < 35:
        return content
    return content[:30] + "..."
