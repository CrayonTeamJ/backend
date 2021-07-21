import json

from requests.api import post
# 사용자 아이디, video pk(number 대체) db에서 가져와서 result.json에 저장해야 함


def to_json(pre_result):
    # json 파일 읽어오기
    # with open('pre_result') as json_file:
    json_data = json.loads(pre_result)
    # print(type(json_data))

    length = len(json_data["segments"])

    # change format of json
    output = {}
    # _id : mongo db에 저장할 때 자동 생성
    output['video_id'] = 'id'  # video_id 는 sql에서 id(video) 가져오기  수정해야함
    output['sentence_list'] = []
    for j in range(length):
        output['sentence_list'].append({
            "sentence_number": j+1,
            "confidence": json_data["segments"][j]["confidence"],
            "sentence": json_data["segments"][j]["text"],
            "start_time": json_data["segments"][j]["start"],
            "end_time": json_data["segments"][j]["end"]
        })
    # print(json.dumps(output, ensure_ascii=False, indent=4))

    return output

    # # json 파일 쓰기
    with open('post_result.json', 'w', encoding='UTF-8-sig') as outfile:
        json.dump(output, outfile, indent=4, ensure_ascii=False)
    # return 'post_result'