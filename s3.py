#!/usr/bin/env python

"""
    Copyright (C) 2012 Bo Zhu http://fun.bozhu.me

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError

from storage import Storage


class S3Bucket(Storage):
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

    def delete_files(self, set_files):
        self.bucket.delete_keys(list(set_files))  # cannot use set here?

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
    from config import config
    aws_key_id = config[0]['aws_key_id']
    aws_key = config[0]['aws_key']
    s3_bucket = config[0]['s3_bucket']

    my_bucket = S3Bucket(aws_key_id, aws_key, s3_bucket)

    my_bucket.upload_files({
        'test1.html': 'test1.html', 'test2.html': 'test2.html'
    })
    print my_bucket.get_value('test1.html')
    my_bucket.delete_files(['test1.html', 'test2.html'])
    print my_bucket.get_value('test1.html')
