from elasticsearch import Elasticsearch
from flask import json, jsonify

es = Elasticsearch(['http://elasticsearch:9200'], http_auth = ('elastic', 'changeme'))

def deleteIndex():
    es.indices.delete(index= '*', ignore=[400,404])

def createIndex():

    if not es.indices.exists(index="contents"):
        es.indices.create(
            index = "contents",
            body = {
                "mappings" : {
                    "properties" : {
                        "video_number" : {"type" : "integer"},
                        "sentence" : {"type" : "text"},
                        "start_time" : {"type" : "integer"}
                    }
                }
            }
        )


def insert_data(input_elastic):

    body = input_elastic
    result = es.index(index='contents', body=body)

def audio_search(video_id, keyword):

    query= {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "video_number": video_id
                        }
                    },
                        {
                        "match": {
                            "sentence": keyword
                        }
                    }
                ]
            }
        },
        "_source": ["start_time"]
    }

    res = es.search(index='contents', body=query)        

    return res