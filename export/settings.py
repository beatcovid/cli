import os

"""
The ACCESS_KEY SECRET_KEY are credentials AWS credentials with write privileges
to BUCKET_NAME.

FORM_ID is a number id of the kobo form to export data from, hosted at
KOBOCAT_API_URI with authorization provided by KOBOCAT_API_CREDENTIALS
"""
ACCESS_KEY = os.environ.get("ACCESS_KEY", default=None)
SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
BUCKET_NAME = os.environ.get("S3_BUCKET", default=None)

FORM_ID = os.environ.get("FORM_ID", "3")

KOBOCAT_API_URI = os.environ.get("KOBOCAT_API", default="https://kc.beatcovid19now.org/")

KOBOCAT_API_CREDENTIALS = os.environ.get("KOBOCAT_CREDENTIALS", default=None)

REDIS_HOST = os.environ.get("REDIS_HOST", default="127.0.0.10")
