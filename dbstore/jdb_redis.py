# !/usr/bin/env python
#
#
from abstract import abstract
import redis
import logging

__author__ = 'Sanctum Networks (P) Ltd.'

jdbe_log = logging.getLogger("jdbe")


class jdb_redis(abstract):
    def __init__(self, *args, **kwargs):
        jdbe_log.debug("jdb_redis:init:")
        jdbe_log.debug("jdb_redis:init:{0} {1}".format(args, kwargs))
        # kwargs["u"]=u
        super(jdb_redis, self).__init__(*args, **kwargs)
        self.u = {}

    def setup(self, u):
        self.u = u
        try:
            self.redis_client = redis.Redis(host=self.u["server"], port=self.u["port"])
            jdbe_log.debug("jdb_redis:setup:u[{0}]:y[{1}]".format(self.u, u))
        except Exception as e:
            jdbe_log.debug("jdb_redis:setup:{}".format(e))
        # super(jdb_redis, self).setup(u)

    def get_redis_client(self):
        return self.redis_client
