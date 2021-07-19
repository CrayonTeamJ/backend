import json
#사용자 아이디, video pk(number 대체) db에서 가져와서 result.json에 저장해야 함

#파일 읽어오기
with open('output.json') as json_file:
    json_data = json.load(json_file)

#video_number 말고 video_pk로 변경
i=1

length= len(json_data["segments"])

list=[]
len = list.append(json_data['segments'])

output = {}
output['_id']='????????' #아이디는 db에서 가져오기
output['video_number']= i #이거 어떻게 할까
output['sentence_list'] = []
for j in range(length) :
    output['sentence_list'].append({
        "sentence_number": j+1,
        "confidence": json_data["segments"][j]["confidence"],
        "sentence": json_data["segments"][j]["text"],
        "start_time": json_data["segments"][j]["start"],
        "end_time": json_data["segments"][j]["end"]
    })

# print(output)

with open('result.json', 'w', encoding='UTF-8-sig') as outfile:
    json.dump(output, outfile, indent=4, ensure_ascii=False)