#!/usr/bin/env python

"""
    Copyright (C) 2012 Bo Zhu http://zhuzhu.org

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

from config import config

from git import GitRepo
from s3 import S3Bucket


VERSION_FILE = '.htautodeploy'


def deploy(repo_name):
    for s in config:
        if s['repo_name'] == repo_name:
            git_repo = GitRepo(
                    remote_url=s['repo_url'],
                    local_folder=s['repo_name'])

            if s['deploy_type'] == 's3':
                server = S3Bucket(
                        s['aws_key_id'],
                        s['aws_key'],
                        s['s3_bucket'])

                prev_hash = server.get_value(VERSION_FILE)
                if '' == prev_hash:
                    files_to_upload = git_repo.all_files()
                    files_to_delete = []
                else:
                    files_to_upload, files_to_delete = \
                            git_repo.changed_files(prev_hash)

                server.upload_files(files_to_upload, all_public=True)
                server.delete_files(files_to_delete)

                server.set_value(VERSION_FILE, git_repo.head_hash())

            elif s['deploy_type'] == 'ssh':
                print 'did nothing'

            else:
                assert False, \
                        'Wrong deploy type: %s. Only support S3 and SSH now' \
                        % s['deploy_type']
            return


if __name__ == '__main__':
    deploy(config[0]['repo_name'])
