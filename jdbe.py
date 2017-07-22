
"""This file is mainly used to parse  .ini config file and making database connection."""
# !/usr/bin/env python
#

import logging
from ConfigParser import ConfigParser
import utils
from dbstore.jdb_mysql import jdb_mysql
from dbstore.jdb_mongodb import jdb_mongodb
from dbstore.jdb_redis import jdb_redis
from dbstore.jdb_elasticsearch import jdb_elasticsearch
import sys
import traceback

__author__ = 'Sanctum Networks (P) Ltd.'


app_log = logging.getLogger("falcon")


# JDB engines


class jdb(jdb_redis, jdb_mysql, jdb_mongodb, jdb_elasticsearch):
    """JDB engine class."""

    def __init__(self):
        """Init method of this class and calling base class init method."""
        super(jdb, self).__init__()

    def setup(self, u, v, w, z):
        """Set up various db source connection."""
        try:
            jdb_redis.setup(self, u)
            jdb_mysql.setup(self, v)
            jdb_mongodb.setup(self, w)
            jdb_elasticsearch.setup(self, z)
        except AttributeError, e:
            app_log.info("jdb:setup: NOIMPL {}".format(e))
            traceback.print_exc(file=sys.stdout)
            sys.stderr.close()


class jdbe:
    def __init__(self, conf):
        app_log.debug("jdbe:init:start Parse {}".format(conf))

        jdbe_ini = ConfigParser()
        jdbe_ini.read(conf)

        self.mongo_ip = jdbe_ini.get('JDBE', 'mongo_ip')
        self.mongo_port = jdbe_ini.get('JDBE', 'mongo_port')
        self.j_mongodb_name = jdbe_ini.get('JDBE', 'jupiter_mongodb_name')

        self.redis_ip = jdbe_ini.get('redis', 'redis_ip')
        self.redis_port = jdbe_ini.get('redis', 'redis_port')

        self.mip = jdbe_ini.get('mysql', 'mysql_ip')
        self.mport = jdbe_ini.get('mysql', 'mysql_port')
        self.muser = jdbe_ini.get('mysql', 'user')
        self.mpassword = jdbe_ini.get('mysql', 'password')

        self.es_ip = jdbe_ini.get('ELASTICSEARCH', 'es_ip')
        self.es_port = jdbe_ini.get('ELASTICSEARCH', 'es_port')

        # Assemble parameters
        self.jdb_redis_params = {
            "server": self.redis_ip,
            "port": self.redis_port
        }
        self.jdb_mongodb_params = {
            "server": self.mongo_ip,
            "port": self.mongo_port,
            "dbname": self.j_mongodb_name
        }
        self.jdb_mysql_params = {
            "server": self.mip,
            "port": self.mport,
            "user": self.muser,
            "password": self.mpassword
        }

        self.jdb_elasticsearch_params = {
            "server": self.es_ip,
            "port": self.es_port,
        }

        app_log.debug("jdbe:init:complete")

    def _check_params(self):
        app_log.debug("jdbe:check:start")
        utils.dump_object(self)
        # raise TypeError, "Parameter error"
        app_log.debug("jdbe:check:complete")

    def start(self):
        app_log.debug("jdbe:start:start")

        #
        # Checkinng var(self) has proper valid json
        self._check_params()

        #
        utils.setup_sighandlers()

        #
        self.jdb = jdb()

        self.jdb.setup(
                self.jdb_redis_params,
                self.jdb_mysql_params,
                self.jdb_mongodb_params,
                self.jdb_elasticsearch_params
                )

        # raise TypeError, "bogus type error for testing"
        #
        app_log.debug("jdbe:start:complete")

    def get_mongodb_connection_auth(self):
        return self.jdb.get_mongodb_client(self.j_mongodb_name)

    def get_redis_connection(self):
        return self.jdb.get_redis_client()

    def get_mysql_connection(self):
        return self.jdb.get_mysql_client()

    def get_elasticsearch_connection(self):
        return self.jdb.get_elasticsearch_client()
