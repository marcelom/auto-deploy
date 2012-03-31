#!/usr/bin/env python

from boto.s3.connection import S3Connection
from boto.s3.key import Key


def upload_to_s3(key_id, key_secret, bucket_name,
        list_files, public_files=True):

    conn = S3Connection(key_id, key_secret)
    buck = conn.get_bucket(bucket_name)

    for file_name in list_files:
        obj = Key(buck, file_name)
        with open(file_name) as fp:
            obj.set_contents_from_file(fp)
        if public_files:
            obj.make_public()

if __name__ == '__main__':
    from setting import AWS_KEY_ID, AWS_KEY, S3_BUCKET
    upload_to_s3(AWS_KEY_ID, AWS_KEY, S3_BUCKET,
            ['test1.html', 'test2.html'])
