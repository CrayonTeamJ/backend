from app import coll2

def image_search(video_id, search_img):
    keyword = search_img

    #검색 키워드 목록
    0 = ['suga','sugar','슈가', '윤기', '민윤기']
    1 = ['jungkook', '정국', '전정국']
    2 = ['colbert']
    3 = ['jimin']
    4 = ['rm']
    5 = ['jin']
    6 = ['v']
    7 = ['jhope']

    #영어일 경우 소문자로 변환
    for c in keyword:
        if not ord('A')<=ord(c)<=ord('z'):
            break
        keyword.lower()

    #클래스 당 몽고디비 검색 결과 가져오기
    # if keyword in 0:
    #     res = coll2.find({"_id":0, "video_number": video_id, "detection_list["class"]:"0" )

    # elif keyword in 1:
    #     coll2.find({'class':1})

    # elif keyword in 2:
    #     coll2.find({'class':2})

    # elif keyword in 3:
    #     coll2.find({'class':3})

    # elif keyword in 4:
    #     coll2.find({'class':4})

    # elif keyword in 5:
    #     coll2.find({'class':5})

    # elif keyword in 6:
    #     coll2.find({'class':6})

    # elif keyword in 7:
    #     coll2.find({'class':7})
    
    # else:
    #     #return fail

    # #5초 이상 나오는 결과의 시작 초 return


    # return