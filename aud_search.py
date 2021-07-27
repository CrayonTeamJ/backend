from elasticsearch import Elasticsearch
from flask import json, jsonify

es = Elasticsearch(['http://elasticsearch:9200'], http_auth=('elastic', 'changeme'))

def createIndex():

        es.indices.create(
            index = "content",
            body = {
                "mappings" : {
                    "properties":{
                        "video_number" : {"type" : "integer"},
                        "sentence_number" : {"type" : "integer"},
                        "sentence" : {"type" : "text"},
                        "start_time" : {"type" : "integer"}
                    }
                }
            }
        )


def insert_data(input_elastic, video_id):

    body = input_elastic
    result = es.index(index='content', body=body, id=video_id)

def audio_search(video_id, keyword):
    
    #mongo db에서 가져오기(index)
    # index = [검색할_인덱스]
    # query_body = [검색할_쿼리문]

    query= {
        "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "video_number": video_id
                                }
                            }
                        ],
                        "query" : {
                            "nested": {
                                "path": "sentence_list",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {
                                                "match": {
                                                    "sentence_list.sentence": keyword
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
        },
        "_source": ["start_time"]
    }

    res = es.search(index='', body=query)
    # res에 검색 결과가 담겨져 있다           

    return res  


    {
        "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "video_number": video_id
                                }
                            },
                            "query" : {
                                "nested": {
                                    "path": "sentence_list",
                                    "query" : {
                                        "match" : {
                                            "sentence_list.sentence": keyword
                                        }
                                    }
                                }
                            }
                        ]
                    }
        },
        "_source": ["start_time"]
    }




     {
        "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "video_number": video_id
                                }
                            }
                        ],
                        "query" : {
                            "nested": {
                                "path": "sentence_list",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {
                                                "match": {
                                                    "sentence_list.sentence": keyword
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
        },
        "_source": ["start_time"]
    }


    query= {
                "query": {
                    "nested":{
                        "path": "sentence_list",
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
                        }
                    }
                },
                "_source": ["start_time"]
    }



    query= {
        "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "video_number": video_id
                                }
                            }
                        ],
                        "query" : {
                            "nested": {
                                "path": "sentence_list",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {
                                                "match": {
                                                    "sentence_list.sentence": keyword
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
        },
        "_source": ["start_time"]
    }


    query = {
        "query" : {
            "nested" : {
                "path" : "characters",
                "query" : {
                    "bool" : {
                        "must" : [
                            {
                                "match": {
                                    "sentence_list.sentence" : keyword
                                }
                            },
                            {
                                "match" : {
                                    "video_number": video_id
                                }
                            }
                        ]
                    }
                }
            }
        }
    }



query = {
  "query": {
    "bool": {
      "must": [
        { 
            "match": { 
                "video_number": video_id 
            }
        },
        {
          "nested": {
              "path" : "sentence_list",
              "query" : {
                  "bool" : {
                      "must" : [
                          {
                              "match" : {
                                  "sentence_list.sentence" : keyword
                              }
                          }
                      ]
                  }
              }
          }
        }
      ]
    }
  }
}


  query = {
        "_source": "sentence_list.start_time",
        "query": {
            "nested":{
                "path": "sentence_list",
                "inner_hits":{},
                "query":{
                    "match": { "sentence_list.start_time": keyword }
                }
            }
        },
        "query":{
            "terms":{
                "_id": [video_id]
            }
        }
    }

    {
  "query": {
    "nested": {
      "path": "sentence_list",
      "query": {
        "bool": {
          "must": [
            { "match": { "user.first": "Alice" }},
            { "match": { "user.last":  "Smith" }} 
          ]
        }
      }
    }
  }
}

{
    "_source" : "sentence_list.start_time",
    "query" : {
        "nested" : "sentence_list",
        "query" : {
            "match" : {
                "sentence_list.sentence" : keyword
            }
        }
    }
    "query" : {
        "terms" : {
            "_id": [video_id]
        }
    }
}
