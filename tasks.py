import models
import views
from flask_celery import make_celery
from app import celery
from app import db
import time
import function.video_func
import requests



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
    time.sleep(5)
    function.video_func.download_audio(youtube_url, file_number)
    time.sleep(5)

@celery.task()
def async_download_video(youtube_url, file_number):
    
    return function.video_func.download_video(youtube_url, file_number)
    
@celery.task()
def post_toYolo(pk, video_path):
    data = {'video_pk': pk, 's3_video': video_path}
    return requests.post('http://0.0.0.0:5001/to_yolo', json=data).content


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