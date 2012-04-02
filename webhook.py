#!/usr/bin/env python

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
    application.listen(8080)

    import tornado.ioloop
    ioloop = tornado.ioloop.IOLoop.instance()
    import tornado.autoreload
    tornado.autoreload.start(ioloop)
    ioloop.start()
