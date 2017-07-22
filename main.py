"""Begining of the program."""

# !/usr/bin/env python

import sys
import os
import platform
import argparse
import logging
import logging.handlers
import time
import utils
import jdbe
from api.router import api_router


__author__ = "Sanctum Networks (P) Ltd."
__copyright__ = "Copyright (C) 2016 Sanctum Networks (P) Ltd."
__revision__ = "$Id"
__version__ = "JDBE 1.0 (Alpha) RC1"


try:
    import psutil
except ImportError:
    raise ImportError("jdbe:main: psutil <sudo pip install psutil>")

dir_path = os.path.dirname(os.path.realpath(__file__))
g_jdbe_log = os.path.join(dir_path, "app.log")
g_jdbe_log_format = '%(asctime)s %(levelname)s %(name)s %(filename)s:%(funcName)s():%(lineno)d %(message)s'

jdbe_log = logging.getLogger()


class JDBEd():
    """Main classes."""

    def set_args(self, a):
        """__setter__ function."""
        self.args = a
        global jdbe_log
        """
        ###############################################
        #### LOGGING CLASS SETTINGS (py25+, py30+) ####
        #### with py23, py24 without 'encoding' arg ###
        ###############################################
        """
        LEVELS = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL,
                  }
        logging.Formatter.converter = time.gmtime
        log_f = logging.Formatter(fmt=g_jdbe_log_format, datefmt="%Y-%m-%d %H:%M:%S")
        log_handlers = [
            logging.handlers.RotatingFileHandler(g_jdbe_log, encoding='utf8',
                                                 maxBytes=10000000, backupCount=3),
            logging.StreamHandler()
        ]
        jdbe_log = logging.getLogger()
        jdbe_log.setLevel(LEVELS.get(self.args.log))
        for h in log_handlers:
            h.setFormatter(log_f)
            h.setLevel(logging.DEBUG)
            jdbe_log.addHandler(h)

        """
        ##############################
        #### END LOGGING SETTINGS ####
        ##############################
        """

    def sys_inventory(self):
        """Package development infoemation including machine architechure.

        platform is a python library to give all these information
        """
        jdbe_log.info("Version      : {}".format(platform.python_version()))
        jdbe_log.info("Version tuple: {}".format(platform.python_version_tuple()))
        jdbe_log.info("Compiler     : {}".format(platform.python_compiler()))
        jdbe_log.info("Build        : {}".format(platform.python_build()))
        jdbe_log.info("System : {}".format(platform.platform()))

        jdbe_log.info("uname: {}".format(platform.uname()))
        jdbe_log.info("system   : {}".format(platform.system()))
        jdbe_log.info("node     : {}".format(platform.node()))
        jdbe_log.info("release  : {}".format(platform.release()))
        jdbe_log.info("version  : {}".format(platform.version()))
        jdbe_log.info("machine  : {}".format(platform.machine()))
        jdbe_log.info("processor: {}".format(platform.processor()))
        jdbe_log.info("interpreter: {}".format(platform.architecture()))

    def sys_state(self):
        """System cpu and memory informations."""
        jdbe_log.info("jdbe:status: CPU:{} MEM:{}% ".format(psutil.cpu_percent(interval=0, percpu=True),
                                                            psutil.virtual_memory()[2]))

    def run(self):
        """Reading .ini configuration file."""
        self.sys_inventory()
        #
        # JDBE
        #
        try:
            # SETTINGS jdbe state in INIT mode by calling utils file function _jdbe_state_set
            utils._jdbe_state_set("INIT")
            self.jdbe = jdbe.jdbe(self.args.jdbe_config_file)
            # Calling jdbe class method start
            self.jdbe.start()
            # calling utils file method propert and SETTINGS state
            utils._jdbe_state_set("RUNNING")
        except Exception:
            jdbe_log.exception("jdbe:exception:Can't instantiate JDBE (FATAL).")
            sys.exit(-1)

        #
        # FALCON
        #
        try:
            # Calling api/router api_router function and then calling setup( with jdbe class object)
            self.falcon1 = api_router()
            self.falcon1.setup(self.jdbe)
            #
            # FIXME: Need a better way of PASSING the db pointer
        except Exception:
            # self.falcon1.setup(self.jdbe)
            jdbe_log.exception("jdbe:exception:Can't instantiate FALCON (FATAL).")
            sys.exit(-1)


def main(argv):
    # https://pymotw.com/2/argparse/
    e = "{} {}".format(__version__, __revision__)
    parser = argparse.ArgumentParser(description="JDBE daemon", epilog=e)

    parser.add_argument("operation", metavar='OPERATION',
                        type=str,
                        help="Operations: start, stop, restart, status",
                        choices=["start", "stop", "restart", "status"])
    parser.add_argument('-c', action='store', dest='jdbe_config_file',
                        help='Config file path (default: /etc/application_name/jdbe.ini)',
                        default='/etc/application_name/jdbe.ini')
    parser.add_argument('--log', type=str, default="debug", help='Log Level')
    parser.add_argument('--version', action='version', version=__version__)

    args = parser.parse_args()
    # print "@@@@@@@@@@@", sys.argv[2]
    utils._jdbe_state_set("START")
    daemon = JDBEd()
    daemon.set_args(args)
    daemon.run()


if __name__ == "__main__":
    main(sys.argv[1:])
