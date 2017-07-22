"""There is only POST API to find record using devide ID and making aggregation on mongo cmtraff collection."""
# !/usr/bin/env python

import falcon
import logging
from utils import api_list
import json

__author__ = 'Sanctum Networks (P) Ltd.'
jdbe_log = logging.getLogger("jdbe")


class listAPI:
    """Class to make aggregation on cmtraff mongodb collection using device ID passed API params."""

    def __init__(self, db):
        """SELF API IUnknown."""
        self.api = ["list-api"]

    def on_get(self, req, resp):
        """Falcon POST api for CM statistics resource manager."""
        try:
            start = req.get_param_as_int('start') or 0
            end = req.get_param_as_int('end') or 10
            result = {}
            result['result'] = api_list[start: end]
            result['count'] = len(api_list)
            resp.status = falcon.HTTP_200
        except:
            result = {"result": "request json key error"}
            resp.status = falcon.HTTP_400
        jdbe_log.debug("Body response:::: {}".format(result))
        print result
        resp.body = json.dumps(result)
