import requests
import json


class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/888/cab16b7c055bf6c6d1188cb2d773b613597f4f7cdafe11f6923f66592015e696'

    # Clova Speech secret key
    secret = 'b662510650de469e864c4caa8350743a'

    def req_url(self, url, language, completion, callback=None, userdata=None, forbiddens=None, boostings=None, sttEnable=True,
                wordAlignment=True, fullText=True, script='', diarization=None, keywordExtraction=None, groupByAudio=False):
        request_body = {
            'url': url,
            'language': language,
            # 'language': 'ko-KR',
            # 'language': 'en-US',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'sttEnable': sttEnable,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'script': script,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'keywordExtraction': keywordExtraction,
            'groupByAudio': groupByAudio,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        res = requests.post(headers=headers,
                            url=self.invoke_url + '/recognizer/url',
                            data=json.dumps(request_body).encode('UTF-8'))
        # print('res.text:', res.text)
        # print('res', res)
        # dict = json.loads(res.text)

        return res.text


# if __name__ == '__main__':
#     res = ClovaSpeechClient().req_url(
#         url='https://teamj-data.s3.ap-northeast-2.amazonaws.com/audio/audio1.mp3', completion='sync')
    # from S3 URL
    # res = ClovaSpeechClient().req_object_storage(data_key='data/media.mp3', completion='sync')
    # res = ClovaSpeechClient().req_upload(file='/data/media.mp3', completion='sync')
    # print(res.text)