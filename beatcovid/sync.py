from datetime import datetime

from smart_open import smart_open as open

BASE_FILENAME = "beatcovidnow"


def get_today_format():
    now = datetime.utcnow()
    return now.strftime("%Y%m%d")


def get_hour_format():
    now = datetime.utcnow()
    return now.strftime("%Y%m%d.%H%M")


def sync_since(dest_path):
    pass


def sync_full(dest_path):
    pass
