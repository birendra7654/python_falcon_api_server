# !/usr/bin/env python

import logging
from abstract import abstract
import pymongo

jdbe_log = logging.getLogger("jdbe")
__author__ = 'Sanctum Networks (P) Ltd.'


class jdb_mongodb(abstract):
    def __init__(self, *args, **kwargs):
        jdbe_log.debug("jdb_mongodb:init:")
        # kwargs["v"]=v
        super(jdb_mongodb, self).__init__(*args, **kwargs)
        self.v = {}

    def setup(self, v):
        self.v = v
        try:
            _con_str = "mongodb://{0}:{1}/".format(self.v["server"], self.v["port"])
            # self.mongodb_client = pymongo.MongoClient(_con_str, connect=False)
            self.mongodb_client = pymongo.MongoClient(_con_str, maxPoolSize=50, waitQueueMultiple=10, connect=False)
            self.mongodb_client[self.v['dbname']].subscriber.create_index("username", unique=True)
            self.mongodb_client[self.v['dbname']].cm.create_index("mac-address", unique=True)
            self.mongodb_client[self.v['dbname']].productprof.create_index("product-id", unique=True)
            jdbe_log.debug("jdb_mongodb:setup:connected {}".format(_con_str))

        except pymongo.errors.ServerSelectionTimeoutError as e:
            jdbe_log.debug("jdb_mongodb:setup:{}".format(e))

    def get_mongodb_client(self, n):
        return self.mongodb_client[n]
