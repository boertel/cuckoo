from redis import StrictRedis


class Redis(object):
    def init_app(self, app):
        self.redis = StrictRedis.from_url(app.config['REDIS_URL'])

    def __getattr__(self, name):
        return getattr(self.redis, name)
