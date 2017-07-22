# !/usr/bin/env python

import falcon
import utils
import logging
import pymongo
import sys
import traceback
# from utils import api_list

__author__ = 'Sanctum Networks (P) Ltd.'

jdbe_log = logging.getLogger("jdbe")


class allPlanResource:
    """All plan resource handler."""

    def __init__(self, db):
        """Intialize DB object to access databases functions."""
        self.api = ["all-plans"]
        self.db = db

    def on_get(self, req, resp):
        try:
            query = {}
            if req.get_param('type'):
                query['type'] = req.get_param('type')
            dbc = self.db.get_mongodb_connection_auth()
            result = list(dbc.productprof.find(query, {"_id": 0,
                                                       "product-id": 1,
                                                       "product-name": 1,
                                                       "price": 1,
                                                       "validity": 1,
                                                       "downstream": 1,
                                                       "upstream": 1,
                                                       "description": 1,
                                                       "type": 1,
                                                       "parameters": 1}))
            result = {"plans": result}
            # resp.set_headers([('date', 'Wed, 18 Sep 2013 16:18:17 GMT'), ('X-Auth-Token', 'ajalkjalkjah')])
            # print resp._headers
            resp.status = falcon.HTTP_200
            # print api_list
            jdbe_log.debug(result)
        except pymongo.errors.ConnectionFailure, e:
            jdbe_log.error("Could not connect to Mongo server: %s" % str(e))
            result = {"error": "Could not connect to Mongo server: %s" % str(e)}
            resp.text = str(traceback.format_exc())
            resp.status = falcon.HTTP_500
        except Exception as e:
            result = {"result": "Some unknown problem"}
            resp.status = falcon.HTTP_400
            jdbe_log.error(traceback.print_exc(file=sys.stdout))
        resp.body = utils.JSONEncoder().encode(result)
        # jdbe_log.debug("Body response {}".format(result))
        # jdbe_log.info("api={0}, response_status={1}".format(self.api[0], resp.status))
