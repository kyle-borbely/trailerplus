import re
from datetime import datetime
from django.utils import timezone
from product.models import Trailer
import pytz

def titeliser(text):
    pattern = re.compile(r"([\w ]+)[.,;:-]")
    match = re.findall(pattern, text)
    try:
        return match[0][:120]
    except IndexError:
        return text[:120]


def get_date(text):
    try:
        regex = r"(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})T(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}).+"
        pattern = re.compile(regex)
        time = pattern.match(text)
        if time is None:
            raise ValueError
        else:
            time_dict = {key: int(value) for key, value in time.groupdict().items()}
            return datetime(**time_dict, tzinfo=pytz.UTC)
    except ValueError:
        regex = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}).+"
        pattern = re.compile(regex)
        time = pattern.match(text)
        if time is None:
            return timezone.now()
        else:
            time_dict = {key: int(value) for key, value in time.groupdict().items()}
            return datetime(**time_dict, tzinfo=pytz.UTC)


def get_trailer(mpn):
    if not len(trailers := Trailer.objects.filter(category__base_type=mpn)):
        return
    else:
        return trailers
