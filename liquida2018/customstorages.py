from django.conf import settings
# from storages.backends.s3boto import S3BotoStorage
from storages.backends.s3boto3 import S3Boto3Storage
import os

os.environ['S3_USE_SIGV4'] = 'True'

class StaticStorage(S3Boto3Storage):
    host = "s3-%s.amazonaws.com" % settings.AWS_REGION

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key, self.secret_key,
                calling_format=self.calling_format, host=self.host)
        return self._connection


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    host = "s3-%s.amazonaws.com" % settings.AWS_REGION

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key, self.secret_key,
                calling_format=self.calling_format, host=self.host)
        return self._connection
