import json
#사용자 아이디, video pk(number 대체) db에서 가져와서 result.json에 저장해야 함

#json 파일 읽어오기
with open('output.json') as json_file:
    json_data = json.load(json_file)



length= len(json_data["segments"])

#change format of json
output = {}
#_id : mongo db에 저장할 때 자동 생성
output['video_id']= 'id'  #video_id 는 sql에서 id(video) 가져오기  수정해야함
output['sentence_list'] = []
for j in range(length) :
    output['sentence_list'].append({
        "sentence_number": j+1,
        "confidence": json_data["segments"][j]["confidence"],
        "sentence": json_data["segments"][j]["text"],
        "start_time": json_data["segments"][j]["start"],
        "end_time": json_data["segments"][j]["end"]
    })


#json 파일 쓰기
with open('result.json', 'w', encoding='UTF-8-sig') as outfile:
    json.dump(output, outfile, indent=4, ensure_ascii=False)