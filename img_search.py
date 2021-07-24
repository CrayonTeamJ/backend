# from app import coll2

def image_search(video_id, keyword):

    #검색 키워드 목록
    suga = ['suga','sugar','슈가', '윤기', '민윤기']
    jungkook = ['jungkook', '정국', '전정국']
    colbert = ['colbert', '콜베어', '콜버트', '스티븐콜베어']
    jimin = ['jimin', '지민', '박지민']
    rm = ['rm', '알엠', '랩몬', '랩몬스터', '남준', '김남준']
    jin = ['jin', '진', '석진', '김석진']
    v = ['v', '뷔', '태형', '김태형']
    jhope = ['jhope', '제이홉', '호석', '정호석']


    # 영어일 경우 소문자로 변환
    for c in keyword:
        if not ord('A')<=ord(c)<=ord('z'):
            break
        keyword2 = keyword.lower()

    print(keyword2)


# image_search(12, 'JungKook')

    #클래스 당 몽고디비 검색 결과 가져오기
    # if keyword in 0:
        # coll2.find({"video_number": video_id}, {detection_list[{"class":'0'}]})

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
