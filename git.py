#!/usr/bin/env python

import subprocess


def check_output(args):
    # learnt from http://goo.gl/CgTnQ
    output = subprocess.Popen(args,
            stdout=subprocess.PIPE).communicate()[0]
    return output

print check_output(['ls', '-l'])
