#!/usr/bin/env python

#
import logging
import utils
from loader import loader
import gunicorn.app.base
from gunicorn.six import iteritems

__author__ = 'Sanctum Networks (P) Ltd.'
app_log = logging.getLogger("falcon")

##
# TODO: MAKE IT CONFIGURABLE
##
JDBE_API_SERVER = "0.0.0.0"
JDBE_API_PORT = 8000
JDBE_API_VERSION = "v0.9"

#
try:
    import falcon
except ImportError:
    raise ImportError("FALCON SERVER <sudo pip install greenlet gevent gunicorn falcon requests>")


# FIXME


def jdbe_gunicorn_cb(environ, start_response):
    global g_falcon_api
    # app_log.debug("api_router:cb:{}".format(environ))
    return g_falcon_api.__call__(environ, start_response)


class jdbe_gunicorn_glue(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(jdbe_gunicorn_glue, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class HandleException(object):
    def __init__(self, jdb_data):
        self.db = jdb_data

    def process_request(self, req, resp):
        """Process the request before routing it.

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """
        pass

    def process_resource(self, req, resp, resource, params):
        """Process the request and resource *after* routing.

        Note:
            This method is only called when the request matches
            a route to a resource.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed. May be None if no route was found for
                the request.
            params: A dict-like object representing any
                additional params derived from the route's URI
                template fields, that will be passed to the
                resource's responder method as keyword
                arguments.
        """
        pass

    def process_response(self, req, resp, resource, req_succeeded):
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
            req_succeeded: True if no exceptions were raised
                while the framework processed and routed the
                request; otherwise False.
        """
        pass


class api_router():
    def __init__(self):
        app_log.debug("falcon:api_router:init: start")
        global g_falcon_api
        app_log.debug("falcon:api_router:init: complete")

    def setup(self, jdb_data):
        global g_falcon_api
        # g_falcon_api = falcon.API(middleware=[HandleException(jdb_data)])
        g_falcon_api = falcon.API()
        app_log.debug("falcon:api_router:setup: start")
        self.loader = loader(g_falcon_api, jdb_data)
        self.loader.setup(JDBE_API_VERSION)

        jdbe_gunicorn_options = {
            "bind": "{}:{}".format(JDBE_API_SERVER, JDBE_API_PORT),
            "workers": utils.number_of_workers(),
            "timeout": 180,
            "worker_class": "gevent",
            "worker_connections": 1000,
            "threads": 3,
        }
        print "!!!!!!!!!!!@@@@@@@@@@", utils.number_of_workers()
        app_log.debug("api_router:falcon:opts:{}".format(jdbe_gunicorn_options))

        jdbe_gunicorn_glue(jdbe_gunicorn_cb, jdbe_gunicorn_options).run()

        app_log.debug("falcon:api_router:setup: complete")
