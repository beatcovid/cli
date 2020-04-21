import os


"""
The ACCESS_KEY SECRET_KEY are credentials AWS credentials with write privileges
to BUCKET_NAME.

FORM_ID is a number id of the kobo form to export data from, hosted at
KOBOCAT_API_URI with authorization provided by KOBOCAT_API_CREDENTIALS
"""
ACCESS_KEY = os.environ.get("ACCESS_KEY", "unknown")
SECRET_KEY = os.environ.get("SECRET_KEY", "unknown")
BUCKET_NAME = os.environ.get("S3_BUCKET", "unknown")

FORM_ID = os.environ.get("FORM_ID", "unknown")

KOBOCAT_API_URI = os.environ.get(
    "KOBOCAT_API", default="https://kc.stopcovid.infotorch.org/"
)

KOBOCAT_API_CREDENTIALS = os.environ.get(
    "KOBOCAT_CREDENTIALS", default="c3VwZXJfYWRtaW46WkxOJEM3WTh6WA=="
)
