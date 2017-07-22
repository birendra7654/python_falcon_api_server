# !/usr/bin/env python

import logging
import mysql.connector
from abstract import abstract
import sys

jdbe_log = logging.getLogger("jdbe")
__author__ = 'Sanctum Networks (P) Ltd.'

# import mysql.connector
# from mysql.connector import Error


class jdb_mysql(abstract):
    """."""

    def __init__(self, *args, **kwargs):
        """."""
        jdbe_log.debug("jdb_mysql:init:")
        # kwargs["w"]=w
        super(jdb_mysql, self).__init__(*args, **kwargs)
        self.w = {}

    def setup(self, w):
        """."""
        self.w = w
        self._db_name = "keystone"
        _con_str = "mysql://{}:{}@{}:{}/{}".format(self.w["user"],
                                                   self.w["password"],
                                                   self.w["server"],
                                                   self.w["port"],
                                                   self._db_name)
        try:
            self.client = mysql.connector.connect(host=self.w["server"],
                                                  port=self.w["port"],
                                                  user=self.w["user"],
                                                  password=self.w["password"],
                                                  database=self._db_name)
            if self.client.is_connected():
                jdbe_log.debug("jdb_mysql:setup:connected {}".format(_con_str))
        except:
            jdbe_log.debug("jdb_mysql:setup:{}".format(sys.exc_info()[0]))

    def get_mysql_client(self):
        return self.client
