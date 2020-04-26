
from huey import RedisHuey, crontab

from export.cli import write_export
from export.settings import REDIS_HOST

huey = RedisHuey('beatcovid.export', host=REDIS_HOST)

@huey.periodic_task(crontab(hour='*/1'))
def hourly_export_dump():
    write_export()
