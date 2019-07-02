# -*- coding: utf-8 -*-
import pymongo
import urllib

def get_mongo_db_client():
    username_str = 'breadt'
    password_str = 'Breadt@2019'

    username = urllib.parse.quote_plus(username_str)
    password = urllib.parse.quote_plus(password_str)

    client = pymongo.MongoClient('mongodb://%s:%s@10.12.86.109:27017/' % (username, password))
    return client