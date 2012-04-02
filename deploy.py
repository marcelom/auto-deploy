#!/usr/bin/env python

from config import settings

from git import GitRepo
from s3 import S3Bucket


VERSION_FILE = '.htautodeploy'


def deploy(repo_name):
    for s in settings:
        if s['repo_name'] == repo_name:
            git_repo = GitRepo(
                    remote_url=s['repo_url'],
                    local_folder=s['repo_name'])

            if s['deploy_type'] == 's3':
                storage = S3Bucket(
                        s['aws_key_id'],
                        s['aws_key'],
                        s['s3_bucket'])

            prev_hash = storage.get_value(VERSION_FILE)
            if '' == prev_hash:
                files_to_upload = git_repo.all_files()
                files_to_delete = []
            else:
                files_to_upload, files_to_delete = \
                        git_repo.changed_files(prev_hash)

            #print files_to_upload
            #print files_to_delete
            storage.upload_files(files_to_upload, all_public=True)
            storage.delete_files(files_to_delete)

            storage.set_value(VERSION_FILE, git_repo.head_hash())

            return


if __name__ == '__main__':
    deploy(settings[0]['repo_name'])
