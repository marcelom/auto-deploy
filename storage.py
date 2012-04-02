#!/usr/bin/env python

from abc import ABCMeta, abstractmethod


class Storage:
    __metaclass__ = ABCMeta

    @abstractmethod
    def upload_files(self, dict_files, all_public=False):
        pass

    @abstractmethod
    def delete_files(self, set_files):
        pass

    @abstractmethod
    def get_value(self, key):
        pass

    @abstractmethod
    def set_value(self, key, value, make_public=False):
        pass


if __name__ == '__main__':
    test_abc = Storage()
