"""Profile file contains product logistics and subscriber details."""
# from JDBE import *
import pymongo
import json

import uuid
import time
import csv
import requests
import ldap.modlist as modlist
import sys
import traceback
import itertools
import utils
import elasticsearch
from elasticsearch_dsl import Search
from bson import ObjectId
try:
    from keystoneclient.v3 import client
except ImportError:
    raise ImportError("ketstoneclient <sudo pip install python-keystoneclient>")
# import JDBE
# import sys
# import os
# import binascii
# import base64
# from ConfigParser import ConfigParser


def ProductProfile_create(db, f):
    """description about product retreieving from mysql and mongo."""
    dbmc = db.get_mongodb_connection_auth()
    # dbsc = db.get_mysql_connection()
    dbmc.productprof.create_index("product-id", unique=True)
    try:
        reader = list(csv.reader(f))
        header = reader.pop(0)
        for row in reader:
            row_dict = dict(zip(header, row))
            try:
                dbmc.productprof.update({
                            "product-id": row_dict["product-id"]
                            }, {
                            "$set": row_dict
                            }, upsert=True)
            except:
                print "Product Name already exists"
    except:
        print "-csv product profile parse"
    finally:
        pass
