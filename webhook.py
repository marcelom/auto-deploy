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

import tornado.web
from tornado.escape import json_decode

import deploy

GitHub_POST_IPs = (
    '207.97.227.253',
    '50.57.128.197',
    '127.0.0.1'
)


class GithubHookHandler(tornado.web.RequestHandler):
    def post(self):
        if self.request.remote_ip not in GitHub_POST_IPs:
            self.send_error(status_code=403)
            return

        self.finish()  # is this necessary?

        payload = json_decode(self.get_argument('payload'))
        repo_name = payload['repository']['name']

        deploy.deploy(repo_name)


application = tornado.web.Application([
    (r"/", GithubHookHandler)
])

if __name__ == "__main__":
    application.listen(80)

    import tornado.ioloop
    ioloop = tornado.ioloop.IOLoop.instance()
    import tornado.autoreload
    tornado.autoreload.start(ioloop)
    ioloop.start()
