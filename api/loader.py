
# !/usr/bin/env python
#
#
import logging
import sys
import os
import imp
from utils import api_list
import importlib
import inspect
import ast

__author__ = 'Sanctum Networks (P) Ltd.'
#
jdbe_log = logging.getLogger("jdbe")


class loader:
    def __init__(self, _falcon, _jdb):
        jdbe_log.info("jdbe:loader:init: start")
        self._falcon = _falcon
        self._jdb = _jdb
        self._api_modules = []
        jdbe_log.info("jdbe:loader:init: complete")

    def dynamic_importer(self, name):
        """Dynamically imports modules / classes."""
        try:
            fp, pathname, description = imp.find_module(name)
        except ImportError:
            jdbe_log.info("jdbe:loader:find_module: unable to locate {}".format(name))
            return (None)
        #
        try:
            apipkg = imp.load_module(name, fp, pathname, description)
        except Exception, e:
            jdbe_log.info("jdbe:loader:load_module: apipkg {}".format(e))
        return apipkg

    def setup(self, apiver):
        jdbe_log.info("jdbe:loader:setup: start")
        f = __file__
        path = os.path.dirname(os.path.realpath(f)) + "/" + apiver
        sys.path.append(path)  # This commend tells you that in which directory you can get your file.
        fname = os.path.basename(os.path.realpath(f))
        _skip_list = ["__init__.py", fname, 'utils.py']
        for root, dirs, files in os.walk(path):
            for source in (s for s in files if s.endswith(".py")):
                if source in _skip_list:
                    continue
                name = os.path.splitext(os.path.basename(source))[0]
                module_ = self.dynamic_importer(str(name))
                if not module_:
                    continue
                source = path + '/' + source
                with open(source, 'r') as f:
                    p = ast.parse(f.read())
                    classes = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
                for class_name in classes:
                    m = getattr(module_, str(class_name))
                    m0 = m(self._jdb)
                    if not m0.api:
                        jdbe_log.info("jdbe:loader:api IUknown not present")
                        continue
                    for a in m0.api:
                        _api = "/{}/{}".format(apiver, a)
                        _o = {
                            "m": str(name),
                            "o": m0,
                            "a": _api,
                        }
                        api_list.append(_api)
                        self._api_modules.append(_o)
                        jdbe_log.info("jdbe:loader:register: {}".format(_o))
                        # install API into Falcon router
                        self._falcon.add_route(_api, m0)
        jdbe_log.info("jdbe:loader:setup: complete")
