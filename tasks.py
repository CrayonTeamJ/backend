from re import T
from celery.signals import task_postrun
import models
import views
from flask_celery import make_celery
from app import celery
from app import db
import time
import function.video_func



@celery.task(bind=True)
def async_user_insert(self, userID, password, userNICK):
    views.user_insert(userID, password, userNICK)

@celery.task(bind=True)
def async_user_login(self, userID, password):
    views.user_login(userID, password)

@celery.task(bind=True)
def async_path_by_local(self, category, title, video_path, audio_path):
    views.path_by_local(category, title, video_path, audio_path)

@celery.task(bind=True)
def async_download_audio(self, youtube_url, file_number):
    time.sleep(5)
    function.video_func.download_audio(youtube_url, file_number)

@celery.task(bind=True)
def async_download_video(self, youtube_url, file_number):
    time.sleep(5)
    function.video_func.download_video(youtube_url, file_number)


# @task_postrun.connect
# def close_session(*args, **kwargs):
#     db.session.remove()




# start celery worker
# celery -A tasks  worker --loglevel=info

# start celery beat
# celery -A tasks.celery beat --loglevel=info

celery.conf.beat_schedule = {
    'asyncReadMsg in every 10 seconds': {
        
        'schedule': 10.0
    },
}