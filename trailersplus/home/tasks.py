from __future__ import absolute_import, unicode_literals

import re
import os
import json
import requests
from celery import shared_task
from .models import Footer
from datetime import date, timedelta

from trailersplus.settings import GEOIP_KEY, GEOIP_PATH
import tarfile
import hashlib

CITIES_URL = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key={GEOIP_KEY}&suffix=tar.gz"
COUNTRY_URL = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key={GEOIP_KEY}&suffix=tar.gz"


@shared_task
def footer_date():
    print("EDITING DATE")
    pattern = re.compile(r"\d+/\d+/\d+")
    new_date = date.today() + timedelta(days=3)
    new_date_str = new_date.strftime("%m/%d/%Y")
    for footer in Footer.objects.all():
        if span := pattern.search(footer.bottom_text).span():
            left = footer.bottom_text[: span[0]]
            right = footer.bottom_text[span[1] :]
            footer.bottom_text = left + new_date_str + right
        if span_en := pattern.search(footer.bottom_text_en).span():
            left = footer.bottom_text_en[: span_en[0]]
            right = footer.bottom_text_en[span_en[1]:]
            footer.bottom_text_en = left + new_date_str + right
        if span_es := pattern.search(footer.bottom_text_es).span():
            left = footer.bottom_text_es[: span_es[0]]
            right = footer.bottom_text_es[span_es[1] :]
            footer.bottom_text_es = left + new_date_str + right
        footer.save()


@shared_task
def update_geoip2():
    if len(os.listdir(GEOIP_PATH)):
        return check_for_updates()
    else:
        download.delay("City")
        download.delay("Country")
        with open(os.path.join(GEOIP_PATH, "last.json"), "w+") as data:
            json.dump(
                {
                    "city": requests.head(CITIES_URL).headers["Last-Modified"],
                    "country": requests.head(COUNTRY_URL).headers["Last-Modified"],
                },
                data,
            )


def check_for_updates():
    with open(os.path.join(GEOIP_PATH, "last.json"), "r") as data:
        current_data = json.load(data)

    new_data = {
        "city": requests.head(CITIES_URL).headers["Last-Modified"],
        "country": requests.head(COUNTRY_URL).headers["Last-Modified"],
    }
    if current_data["city"] != new_data["city"]:
        download.delay("City")
    if current_data["country"] != new_data["country"]:
        download.delay("Country")
    with open(os.path.join(GEOIP_PATH, "last.json"), "w") as data:
        json.dump(new_data, data)
    return


@shared_task(bind=True, default_retry_delay=60 * 30)
def download(self, file_type):
    try:
        if file_type == "City":
            URL = CITIES_URL
        elif file_type == "Country":
            URL = COUNTRY_URL
        else:
            raise ValueError(f"{file_type} is not valid type")
        with open(
            os.path.join(GEOIP_PATH, f"GeoLite2-{file_type}.tar.gz"), "wb"
        ) as archive:
            bytes = requests.get(URL).content
            archive.write(bytes)
            hash_d = hashlib.sha256(bytes).hexdigest()
        hash_e = requests.get(URL + ".sha256").content.split()
        if hash_d == hash_e[0].decode("utf-8"):
            with tarfile.open(
                os.path.join(GEOIP_PATH, f"GeoLite2-{file_type}.tar.gz")
            ) as tar:
                for member in tar.getmembers():
                    if member.name.endswith(".mmdb"):
                        with open(
                            os.path.join(GEOIP_PATH, f"GeoLite2-{file_type}.mmdb"), "wb"
                        ) as db:
                            db.write(tar.extractfile(member=member).read())
            os.remove(os.path.join(GEOIP_PATH, f"GeoLite2-{file_type}.tar.gz"))
        else:
            raise requests.exceptions.StreamConsumedError
    except (
        requests.exceptions.StreamConsumedError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.Timeout,
    ):
        self.retry()
