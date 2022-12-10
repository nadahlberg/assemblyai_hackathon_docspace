from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'docspace'
    location = 'media'
    default_acl = 'private'


class StaticStorage(S3Boto3Storage):
    bucket_name = 'docspace'
    location = 'static'
    default_acl = 'public-read'
