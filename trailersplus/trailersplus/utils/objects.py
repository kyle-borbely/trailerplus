from __future__ import annotations

from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from product.models import Location
from collections import defaultdict
from django.db.models import Q
from typing import List, Dict, Tuple
from datetime import datetime, date, timedelta
import time
from product.models import Trailer, CategoryMap


def list_locations() -> Tuple[List, int]:
    locations = defaultdict(list)
    all_stores = Location.objects.filter(active=True)
    for store in all_stores:
        locations[store.get_state_display()].append(
            {"city": store.store_city, "state": store.state, "id": store.store_id, "slug": store.get_slug(), "city_name": store.get_city_name()}
        )
    result = []
    for full_state, stores in locations.items():
        result.append((full_state, sorted(stores, key=lambda x: x['city_name'])))
    return sorted(result), len(all_stores)


def get_my_store(store_id: str) -> Dict[str, str]:
    store = Location.objects.get(store_id=store_id)
    return {"id": store_id,
            "state": store.state,
            "full_state": store.get_state_display(),
            "city": store.store_city,
            "phone": store.store_phone,
            "slug": store.get_slug(),
            "city_name": store.get_city_name(),
            "map_url": store.store_map_url,
            "count": _get_store_trailers(store).count(),
            }


def multiple_q(lst: List[Dict[str, str]]) -> Q:
    if not len(lst):
        return Q()
    elif len(lst) == 1:
        return Q(**lst[0])
    else:
        return Q(**lst[0]) | multiple_q(lst[1:])


def work_hours_table(work_hours: dict,
                     translations,
                     group,
                     language=get_language()):
    order = ["monday_hours", "tuesday_hours", "wednesday_hours", "thursday_hours", "friday_hours", "saturday_hours", "sunday_hours"]
    data = None
    groups = []
    for day in order:
        if data is None:
            data = "monday_hours", None, work_hours["monday_hours"]
        else:
            if work_hours[day] == data[2]:
                data = data[0], day, data[2]
                if day == "sunday_hours":
                    days = group(data)
                    groups.append((days, data[2]))
            else:
                days = group(data)
                groups.append((days, data[2]))
                data = day, None, work_hours[day]
                if day == "sunday_hours":
                    days = group(data)
                    groups.append((days, data[2]))
    table = []
    for days, hours in groups:
        table.append(f"<tr>    <td>{days.replace('_hours', ':')}</td>\n    <td>{hours}</td>\n</tr>")
    if language == 'es':
        for index, row in enumerate(table):
            for what, on in translations.items():
                row = row.replace(what, on)
            table[index] = row
    return mark_safe('\n'.join(table))


def get_time_ago(d1):
    d2 = datetime.now()

    d1_ts = time.mktime(d1.timetuple())
    d2_ts = time.mktime(d2.timetuple())

    time_ago = int(d2_ts - d1_ts)
    if time_ago < 60:
        name = "second"
    else:
        time_ago //= 60
        if time_ago < 60:
            name = "minute"
        else:
            time_ago //= 60
            if time_ago < 24:
                name = "hour"
            else:
                time_ago //= 24
                name = "day"
    if time_ago > 1:
        name += "s"
    return f"{time_ago} {name} ago"


def _get_store_trailers(store):
    normal_filters = [Q(store=store), Q(status__in=(100, 120))]
    sold_filters = [Q(store=store), Q(status__exact=150), Q(sale_date__gte=(date.today() - timedelta(days=14)))]
    trailers = Trailer.objects.none()
    for category in CategoryMap.objects.prefetch_related('include', 'exclude').all():
        category_trailers = Trailer.objects.prefetch_related('trailertranslation_set').filter(*normal_filters + [multiple_q(_form_q_filters(category.include.all())) &~ multiple_q(_form_q_filters(category.exclude.all()))])
        if category_trailers:
            trailers |= category_trailers
            trailers |= Trailer.objects.prefetch_related('trailertranslation_set').filter(*sold_filters + [multiple_q(_form_q_filters(category.include.all())) &~ multiple_q(_form_q_filters(category.exclude.all()))])[:12]
    return trailers


def _form_q_filters(query_set):
    result = []
    for category_filter in query_set:
        pre_template = category_filter.field_name
        if category_filter.case_sensitive:
            template = pre_template + '__'
        else:
            template = pre_template + '__i'
        result.append({f'{template}{category_filter.type}': category_filter.filter})
    return result