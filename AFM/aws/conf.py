import datetime
from decouple import config
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_QUERYSTRING_EXPIRE = 1800
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'AFM.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'AFM.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'tag-afm-bucket'
AWS_S3_REGION_NAME = 'ap-south-1'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static-afi/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")
AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}
AWS_S3_SIGNATURE_VERSION = "s3v4"
