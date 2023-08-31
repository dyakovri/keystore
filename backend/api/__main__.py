import argparse

import gunicorn.app.base

from api.routes.base import app


class HttpServer(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-workers', type=int, default=5)
    parser.add_argument('--port', type=str, default='8080')
    args = parser.parse_args()
    options = {
        'bind': '%s:%s' % ('0.0.0.0', args.port),
        'workers': args.num_workers,
    }
    HttpServer(app, options).run()
