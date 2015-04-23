from game_website import local_settings
AWS_STORAGE_BUCKET_NAME = 'gamewebsitebucket'
AWS_ACCESS_KEY_ID = local_settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = local_settings.AWS_SECRET_KEY
AWS_S3_HOST = 's3-us-west-2.amazonaws.com'
# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'game_website.custom_storages.MediaStorage'

ALLOWED_HOSTS = ['*']
DEBUG = False
