#!/usr/bin/env python

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError


class S3Bucket:
    def __init__(self, key_id, key_secret, bucket_name):
        conn = S3Connection(key_id, key_secret)
        self.bucket = conn.get_bucket(bucket_name)

    def upload_files(self, dict_files, all_public=False):
        # dict of files, {name: local_location}
        for file_name in dict_files.keys():
            obj = Key(self.bucket, file_name)
            with open(dict_files[file_name]) as fp:
                obj.set_contents_from_file(fp)
            if all_public:
                obj.make_public()

    def delete_files(self, list_files):
        self.bucket.delete_keys(list_files)

    def get_value(self, key):
        obj = Key(self.bucket, key)
        try:
            return obj.get_contents_as_string()
        except S3ResponseError as e:
            if e.status == 404:  # not found
                return ''

    def set_value(self, key, value, make_public=False):
        obj = Key(self.bucket, key)
        obj.set_contents_from_string(value)
        if make_public:
            obj.make_public()


if __name__ == '__main__':
    from config import settings
    aws_key_id = settings[0]['aws_key_id']
    aws_key = settings[0]['aws_key']
    s3_bucket = settings[0]['s3_bucket']

    my_bucket = S3Bucket(aws_key_id, aws_key, s3_bucket)

    my_bucket.upload_files({
        'test1.html': 'test1.html', 'test2.html': 'test2.html'})
    print my_bucket.get_value('test1.html')
    my_bucket.delete_files(['test1.html', 'test2.html'])
    print my_bucket.get_value('test1.html')
