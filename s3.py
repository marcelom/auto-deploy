#!/usr/bin/env python

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError


class S3Bucket:
    def __init__(self, key_id, key_secret, bucket_name):
        conn = S3Connection(key_id, key_secret)
        self.bucket = conn.get_bucket(bucket_name)

    def upload_files(self, list_files, all_public=True):
        for file_name in list_files:
            obj = Key(self.bucket, file_name)
            with open(file_name) as fp:
                obj.set_contents_from_file(fp)
            if all_public:
                obj.make_public()

    def get_value(self, key):
        obj = Key(self.bucket, key)
        try:
            return obj.get_contents_as_string()
        except S3ResponseError as e:
            if e.status == 404:  # not found
                return ''

    def set_value(self, key, value, make_public=True):
        obj = Key(self.bucket, key)
        obj.set_contents_from_string(value)
        if make_public:
            obj.make_public()


if __name__ == '__main__':
    from setting import AWS_KEY_ID, AWS_KEY, S3_BUCKET
    my_bucket = S3Bucket(AWS_KEY_ID, AWS_KEY, S3_BUCKET)
    #my_bucket.upload_files(['test1.html', 'test2.html'])
    #print my_bucket.get_value('test.file')
    print my_bucket.get_value('test1.html')
