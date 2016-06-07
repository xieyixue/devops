#!/usr/bin/env python
# coding=utf-8
__author__ = 'xieyixue'

from datetime import datetime
from elasticsearch import Elasticsearch

# import requests
#
# url = 'http://118.192.152.109:9200/megacorp/employee/1'
# data = {
#     "first_name" : "John",
#     "last_name" :  "Smith",
#     "age" :        25,
#     "about" :      "I love to go rock climbing",
#     "interests": [ "sports", "music" ]
# }
#
# r = requests.put(url, data)
# print r.content

es = Elasticsearch(hosts="118.192.152.109")
print es.index(
    index="my-index",
    doc_type="test-type",
    id=42,
    body={"any": "data", "timestamp": datetime.now()})
