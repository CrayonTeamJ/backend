from elasticsearch import Elasticsearch
from flask import json, jsonify

def insert_data(es, input_elastic):

    body = input_elastic
    result = es.index(index='contentb', body=body)

def audio_search(es, video_id, keyword):

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

    res = es.search(index='contentb', body=query)        

    return res