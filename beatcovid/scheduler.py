
from huey import RedisHuey, crontab

from export.cloud_save import s3_save_diff, s3_save_full
from export.settings import REDIS_HOST

huey = RedisHuey('beatcovid.export', host=REDIS_HOST)

@huey.periodic_task(crontab(hour='*/1', minute="0"))
def hourly_export_dump():
    s3_save_diff()
