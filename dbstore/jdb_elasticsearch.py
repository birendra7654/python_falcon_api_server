# !/usr/bin/env python

import logging
from abstract import abstract
from elasticsearch import Elasticsearch

jdbe_log = logging.getLogger("jdbe")
__author__ = 'Sanctum Networks (P) Ltd.'


class jdb_elasticsearch(abstract):
    def __init__(self, *args, **kwargs):
        jdbe_log.debug("jdb_elasticsearch:init:")
        # kwargs["v"]=v
        super(jdb_elasticsearch, self).__init__(*args, **kwargs)
        self.v = {}

    def setup(self, v):
        self.v = v
        try:
            url = "%s:%s" % (self.v['server'], self.v['port'])
            self.elasticsearch_client = Elasticsearch(url, timeout=60,
                                                      max_retries=3,
                                                      retry_on_timeout=True)
            jdbe_log.info("elasticsearch_client connection established")
        except Exception as e:

            jdbe_log.debug("jdb_elasticsearch:setup exception:{}".format(e))

    def get_elasticsearch_client(self):
        return self.elasticsearch_client
