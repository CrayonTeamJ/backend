from elasticsearch import Elasticsearch
import json
from app import coll

def audio_search(video_id, search_aud):
    es = Elasticsearch('http://elasticsearch:9200')
    
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
                            "sentence_list.sentence": search_aud
                        }
                    }
                ]
            }
        },
        "_source": ["start_time"]
    }

    query_body = json.loads(query)

    res = es.search(index='', body=query_body)
    # res에 검색 결과가 담겨져 있다           

    return res  


# coll.find({ $and: [{video_number:video_pk}, {detection_list.class:0}]}).pretty()