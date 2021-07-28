from elasticsearch import Elasticsearch
from flask import json, jsonify

es = Elasticsearch(['http://elasticsearch:9200'], http_auth = ('elastic', 'changeme'))

def createIndex():
    #createIndex in ES
    es.indices.create(
        index = "contentd",
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
    result = es.index(index='contentd', body=body)

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

    res = es.search(index='contentd', body=query)        

    return res