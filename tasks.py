
from pymongo.common import validate_ok_for_update
import views
from flask_celery import make_celery
from app import celery
from app import db
from function.clova_func import *
from function.trans import *
import time
import function.video_func
import requests
import asyncio



@celery.task(bind=True)
def async_user_insert(self, userID, password, userNICK):
    views.user_insert(userID, password, userNICK)

@celery.task(bind=True)
def async_user_login(self, userID, password):
    views.user_login(userID, password)

@celery.task(bind=True)
def async_path_by_local(self, category, title, video_path, audio_path):
    views.path_by_local(category, title, video_path, audio_path)

@celery.task()
def async_download_audio(youtube_url, file_number): 
    function.video_func.download_audio(youtube_url, file_number)
    

@celery.task()
def async_download_video(youtube_url, file_number):
    
    return function.video_func.download_video(youtube_url, file_number)
    
@celery.task()
def post_toYolo(pk, video_path):
    data = {'video_pk': pk, 's3_video': video_path}
    return requests.post('http://0.0.0.0:5001/to_yolo', json=data).content




#===============================================================================================
#여기부턴 asynd 함수
from app import coll

def save_audio_result_to_mongo(video_pk, post_result):
    coll.insert({
        'video_number': video_pk,
        'sentence_list': post_result['sentence_list']
    })

def clova(audio_path, lang):
    pre_result = ClovaSpeechClient().req_url(url=audio_path, language = lang, completion='sync')
        # print('type_of_preresult:', type(pre_result))
    
    post_result = to_json(pre_result)
        # print('type_of_postresult:', type(post_result))
    return post_result

def send_to_yolo(video_path, video_pk):
    data = {"video_path": video_path, "video_pk": video_pk}
    response = requests.post('http://backend_model:5050/to_yolo', json=data, verify=False)
    

async def run_clova(video_pk, audio_path, lang):

    post_result = clova(audio_path, lang)
    save_audio_result_to_mongo(video_pk, post_result)
    return 

async def run_yolo(video_path, video_pk):
    send_to_yolo(video_path, video_pk)

async def detect_clovd(video_pk, audio_path, lang):
    await run_clova(video_pk, audio_path, lang)

async def detect_yolo(video_path, video_pk):
    await send_to_yolo(video_path, video_pk)

async def detect_start(video_pk, audio_path, video_path, lang):

    await run_yolo(video_path, video_pk)
    await run_clova(video_pk, audio_path, lang)

    pass





# @task_postrun.connect
# def close_session(*args, **kwargs):
#     db.session.remove()




# start celery worker
# celery -A tasks  worker --loglevel=info

# start celery beat
# celery -A tasks.celery beat --loglevel=info
@celery.task
def slow_task(x):
	time.sleep(x)
	return x
    


@celery.task
def quick_task(x):
	return x

celery.conf.beat_schedule = {
    'asyncReadMsg in every 10 seconds': {
        
        'schedule': 10.0
    },
}