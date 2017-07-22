"""Utility modules files."""


# !/usr/bin/env python
#
import logging
import signal
import json
from bson import ObjectId

__author__ = 'Sanctum Networks (P) Ltd.'

ja_port = 8080
jdbe_log = logging.getLogger("jdbe")
api_list = []  # listing out all JDBE API


def dump_object(o):
    """Dumping into json object."""
    import json
    return json.dumps(o, default=lambda obj: vars(obj), indent=4)
#


g_jdbe_state = ""


def _jdbe_state_set(s):
    global g_jdbe_state
    g_jdbe_state = s


def handle_SIGINT(signum, stack):
    """Handle process through signal."""
    # Don't know what is happening
    jdbe_log.debug("SIGINT")
    _jdbe_state_set("SIGNAL")


g_signal_handlers = [
    {"signal": signal.SIGINT, "handler": handle_SIGINT}
]


def setup_sighandlers():
    """Set up Signal handlers."""
    jdbe_log.debug("setup signal handlers")
    for s in g_signal_handlers:
        signal.signal(s["signal"], s["handler"])


def number_of_workers():
    """Finding number of worker to run in gunicorn."""
    import multiprocessing
    return (multiprocessing.cpu_count() * 2) + 1


class JSONEncoder(json.JSONEncoder):
    """JSON encoding format."""

    def default(self, o):
        """Method."""
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def validateKeysInJSON(keyList=[], argJSON={}):
    for key in keyList:
        if key not in argJSON:
            raise KeyError("{} not present in JSON::: {}".format(key, argJSON))
