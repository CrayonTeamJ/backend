import requests
import json
import os


class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = os.environ['clova_URL']

    # Clova Speech secret key
    secret = os.environ['clova_secret_key']

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


    # from S3 URL
    # res = ClovaSpeechClient().req_object_storage(data_key='data/media.mp3', completion='sync')
    # res = ClovaSpeechClient().req_upload(file='/data/media.mp3', completion='sync')
    # print(res.text)