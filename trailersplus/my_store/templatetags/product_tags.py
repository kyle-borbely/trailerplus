from django import template
from django.template.defaultfilters import stringfilter
import re
from math import ceil
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from product.models import CategoryMap
from trailersplus.utils.objects import work_hours_table


register = template.Library()


@register.filter
def str_price(price):
    try:
        return f"${int(price)}"
    except ValueError:
        return price


@register.filter
def num_length(length):
    return int(re.match(r'\d+', length).group())


@register.filter
def num_price(price):
    try:
        return int(price)
    except ValueError:
        return price


@register.filter
def formula(price) -> float:
    try:
        pattern = re.compile(r'(\d+\.\d+)')
        dec_price = float(pattern.search(price).group())
    except AttributeError:
        try:
            dec_price = float(price)
        except ValueError:
            return 0.0
    value = ((0.0849/12)*dec_price)/(1-((1+(0.0849/12))**(-48)))
    return ceil(value*100) / 100


@register.filter
def off_formula(sale_price, cash_price):
    # pattern = re.compile(r'(\d+\.\d+)')
    # dec_cash_price = float(pattern.search(cash_price).group())
    return round(float(sale_price) - float(cash_price))


STORE_WORK_HOURS_TRANSLATION = {
        'Closed': 'Cerrado',
        'Set Appointment': 'Programar Cita',
        'Mon': 'Lun',
        'Tue': 'Mar',
        'Wed': 'Mié',
        'Thu': 'Jue',
        'Fri': 'Vie',
        'Sat': 'Sáb',
        'Sun': 'Dom',
}


def group_and_capitalize(data):
    if data[1] is None:
        return data[0][:3] + ':'.capitalize()
    else:
        return f"{data[0][:3].capitalize()} - {data[1][:3].capitalize()}:"


@register.filter
def group_work_hours(work_hours: dict):
    return work_hours_table(work_hours, STORE_WORK_HOURS_TRANSLATION, group_and_capitalize, get_language())


@register.filter
@stringfilter
def underscore(string: str) -> str:
    return string.replace(' ', '_')


@register.filter
@stringfilter
def translate(value: str) -> str:
    language = get_language()
    translate = {
        "all types": "Todos Los Modelos",
        "cargo": "Carga",
        "utility": "Utilitario",
        "car hauler": "Porta vehiculos",
        "snow / atv": "Nieve / ATV",
        "enclosed": "Cerrado",
        "flatbed": "Plano",
        "dump": "Dump",
        "equipment": "Equipo",
    }
    for category in CategoryMap.objects.all():
        translate.update(category.translations)
    if language.lower() == 'es':
        value = value.lower()
        for key, translation in translate.items():
            if key in value:
                value = value.replace(key, translation)
        return value
    else:
        return value


@register.filter
def off_text_template(text, price):
    price = str(price)
    text = text.replace('&lt;off_price&gt;', price)
    text = text.replace('<off_price>', price)
    return text


@register.filter
def phone_number_template(text, number):
    number = str(number)
    text = text.replace('&lt;phone_number&gt;', number)
    text = text.replace('<phone_number>', number)
    return text


@register.filter
def calculate_dimensions(size):
    feet, inch = int(size) // 12, int(size) % 12
    return f'{feet}\' {inch}\"' if feet > 0 else f'{inch}\"'


@register.filter
@stringfilter
def directions_cut(text):
    separator = re.compile(r'\s?<\s?br{1}\s?/{1}\s?>\s?')
    open_b_pattern = re.compile(r'<\s?b\s?>\s?')
    close_b_pattern = re.compile(r'\s?<\s?/{1}\s?b\s?>')
    # if get_language() == 'es':
    #     text = re.sub(r'(<\s?b\s?>\s?)?Direct(\s?<\s?/{1}\s?b\s?>)?\s+', '', text)
    directions_list = separator.split(text)
    result = []
    for direction in directions_list:
        direction = close_b_pattern.sub('</strong> ', direction)
        direction = open_b_pattern.sub('<strong>', direction)
        result.append(direction)
    return '<br>'.join(result)


@register.filter
def my_store_product_title(_1_2, _3):
    title = _3
    count, store_name = _1_2
    count_template = re.compile(r'(&lt;|<)\s?count\s?(&gt;|>)')
    store_name_template = re.compile(r'(&lt;|<)\s?store\s?(&gt;|>)')
    title = count_template.sub(str(count), title)
    title = store_name_template.sub(str(store_name), title)
    title = re.sub("[()'')]", '', title)
    return title


@register.filter
def extend_title(title, vin):
    translations = {'inter': {'en': ' Interstate ', 'es': ' Interestatal '},
                    'karavan': {'en': 'Karavan', 'es': 'Karavan'},
                    'trailer': {'en': ' Trailer', 'es': ' Remolque'},
                    'carry': {'en': ' Carry-On ', 'es': ' Carry-On '},
                    }
    if str(vin).startswith('4RA'):
        addon = translations['inter'][get_language()] \
            if all(name.lower() not in title.lower() for name in ('Inerstate', 'Interestatal')) \
            else ' '
    if str(vin).startswith('5KT'):
        addon = translations['karavan'][get_language()] \
            if all(name.lower() not in title.lower() for name in ('Karavan', 'Karavan')) \
            else ' '
    elif str(vin).startswith('4YM'):
        addon = translations['carry'][get_language()] \
            if all(name.lower() not in title.lower() for name in ('Carry-On', 'Carry-On')) \
            else ' '
    else:
        addon = ' '
    postfix = translations['trailer'][get_language()] \
        if all(name.lower() not in title.lower() for name in ('Trailer', 'Remolque')) \
        else ''

    pattern = re.compile(r'(\d+)((([,.])\d+)?)(\s?)([xX])(\s?)(\d+)((([,.])\d+)?)')
    try:
        span = pattern.search(title).span()
        if get_language() == 'en':
            if vin.startswith('carry_on_vin'):
                return addon + postfix
            else:
                return title[:span[1]] + addon + title[span[1] + 1:] + postfix
        else:
            if vin.startswith('carry_on_vin'):
                return addon + postfix
            else:
                return title[:span[0] - 1] + addon + title[span[0]:] + postfix
    except AttributeError:
        return title + addon + postfix
