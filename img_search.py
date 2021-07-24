from app import coll2
from collections import OrderedDict

def image_search(video_id, keyword):
    
    keyword_list=OrderedDict()

    suga = ['suga','sugar','슈가', '윤기', '민윤기']
    jungkook = ['jungkook', '정국', '전정국']
    colbert = ['colbert', '콜베어', '콜버트', '스티븐콜베어']
    jimin = ['jimin', '지민', '박지민']
    rm = ['rm', '알엠', '랩몬', '랩몬스터', '남준', '김남준']
    jin = ['jin', '진', '석진', '김석진']
    v = ['v', '뷔', '태형', '김태형']
    jhope = ['jhope', '제이홉', '호석', '정호석']

    keyword_list[0] = suga
    keyword_list[1] = jungkook
    keyword_list[2] = colbert
    keyword_list[3] = jimin
    keyword_list[4] = rm
    keyword_list[5] = jin
    keyword_list[6] = v
    keyword_list[7] = jhope

    for c in keyword:
        if not ord('A')<=ord(c)<=ord('z'):
            keyword2 = keyword
            break
        keyword2 = keyword.lower()

    for i in keyword_list:
        if keyword2 in keyword_list[i]:
            return search_from_mongo(video_id, i)

    empty_list=[]
    return empty_list

def search_from_mongo(video_id, class_num):
    detected_seconds = []
    for s in coll2.find({"video_number":video_id}):
            detection_list = s['detection_list']
            for key in detection_list:
                if key['class'] == class_num:
                    detected_seconds.append(key['start_time'])
    return detected_seconds