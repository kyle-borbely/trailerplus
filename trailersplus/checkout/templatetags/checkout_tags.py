from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from datetime import datetime, timedelta

register = template.Library()


@register.filter
def long_text_template(_1_2_3, _4):
    text = str(_4)
    spanish_months = [
        ("January", "Enero"),
        ("February", "Febrero"),
        ("March", "Marzo"),
        ("April", "Abril"),
        ("May", "Mayo"),
        ("June", "Junio"),
        ("July", "Julio"),
        ("August", "Agosto"),
        ("September", "Septiembre"),
        ("October", "Octubre"),
        ("November", "Noviembre"),
        ("December", "Diciembre"),
    ]

    (invoice_date, store_phone), customer_email, = _1_2_3
    plus_7_days = invoice_date + timedelta(days=7)

    text = text.replace('&lt;date&gt;', plus_7_days.strftime('%B %-d, %Y'))
    text = text.replace('&lt;email&gt;', f'<a href="mailto:{customer_email}">{customer_email}</a>')
    text = text.replace('&lt;phone&gt;', f'<a href="tel:{store_phone}">{store_phone}</a>')

    if get_language() == 'es':
        for replacement in spanish_months:
            text = text.replace(*replacement)

    return mark_safe(text.replace('&lt;', '<').replace('&gt;', '>'))


@register.filter
def to_tag(text):
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('<i>', '')
    text = text.replace('</i>', '')
    text = text.replace('<p>', '')
    text = text.replace('</p>', '')
    return mark_safe(text)


@register.filter
def timestamp_to_date(timestamp):
    try:
        # assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
