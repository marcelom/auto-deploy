#!/usr/bin/env python

import tornado.web
from tornado.escape import json_decode

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
        repo_hash = payload['head_commit']['id']

        print repo_name, repo_hash


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
