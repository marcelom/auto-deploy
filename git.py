#!/usr/bin/env python

import subprocess
import os

GIT_LOCAL_BASE = 'repos'
if not os.path.exists(GIT_LOCAL_BASE):
    os.mkdir(GIT_LOCAL_BASE)


def command_output(args):
    # learnt from http://goo.gl/CgTnQ
    output = subprocess.Popen(args,
            stdout=subprocess.PIPE).communicate()[0]
    return output


class GitRepo:
    def __init__(self, remote_url, local_folder):
        self.remote_url = remote_url
        self.local_path = GIT_LOCAL_BASE + '/' + local_folder
        if not os.path.exists(self.local_path):
            self.clone()
        else:
            self.pull()

    def clone(self):
        subprocess.call(['git', 'clone', self.remote_url, self.local_path])

    def pull(self):
        # check http://goo.gl/TQGyY
        # is git still buggy?
        # cannot pull out of working directory
        subprocess.call(['git',
            '--git-dir', self.local_path + '/.git',
            'fetch'])
        subprocess.call(['git',
            '--git-dir', self.local_path + '/.git',
            '--work-tree', self.local_path,
            'merge', '--ff-only', 'origin/master'])

    def changed_files(self, hash1, hash2='HEAD'):
        """
        return lists of updated files and deleted files seperately
        """
        set_deleted = set(command_output(['git',
            '--git-dir', self.local_path + '/.git',
            'diff', '--name-only', '--diff-filter=D',
            hash1, hash2]
        ).strip().split())

        set_changed = set(command_output(['git',
            '--git-dir', self.local_path + '/.git',
            'diff', '--name-only',
            hash1, hash2]
        ).strip().split())

        set_updated = set_changed - set_deleted

        return (
            [self.local_path + '/' + f for f in set_updated],
            [self.local_path + '/' + f for f in set_deleted],
        )


if __name__ == '__main__':
    from config import GIT_REMOTE_URL, GIT_LOCAL_FOLDER
    my_repo = GitRepo(GIT_REMOTE_URL, GIT_LOCAL_FOLDER)
    print my_repo.changed_files('HEAD~2')
