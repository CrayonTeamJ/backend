from elasticsearch import Elasticsearch
from flask import json, jsonify

es = Elasticsearch(['http://elasticsearch:9200'], http_auth=('elastic', 'changeme'))

def createIndex():
        # ===============
        # 인덱스 생성
        # ===============
        es.indices.create(
            index = "content",
            body = {
                "mappings" : {
                    "properties":{
                        "video_number" : {"type" : "integer"},
                        "sentence_list" : {
                            "properties": {
                                "sentence_number" : {
                                    "type": "long"
                                },
                                "confidence" : {
                                    "type": "float"
                                },
                                "sentence" : {
                                    "type": "text"
                                },
                                "start_time" : {
                                    "type": "long"
                                },
                                "end_time" : {
                                    "type": "long"
                                }
                            }
                        }
                    }
                }
            }
        )


def insert_data(input_elastic):

    body = input_elastic
    result = es.index(index='content', body=body)

def audio_search(video_id, keyword):
    
    #mongo db에서 가져오기(index)
    # index = [검색할_인덱스]
    # query_body = [검색할_쿼리문]


 # video_pk가 18이고 sentence에 “고양이”가 나오는 start time을 말해줘!
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
                            "sentence_list.sentence": keyword
                        }
                    }
                ]
            }
        },
        "_source": ["start_time"]
    }

    res = es.search(index='', body=query)
    # res에 검색 결과가 담겨져 있다           

    return res  