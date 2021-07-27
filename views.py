from operator import ne
import sys, os
from sqlalchemy import sql, func, select
from sqlalchemy.sql.expression import false
os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
import models
from app import app, db
import bcrypt
from flask_sqlalchemy import SQLAlchemy

userDB = models.user_info




def user_insert(userID, password, userNICK):
    user_byID = userDB.query.filter(userID == userDB.user_id).first()
    user_byNK = userDB.query.filter(userNICK == userDB.user_nick).first()
    bytes_password = password.encode('UTF-8')
    bytes_hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
    
    if user_byID is None and user_byNK is None:
        new_user = userDB(userID, bytes_hashed_password.decode('UTF-8'), userNICK)
        db.session.add(new_user)
        db.session.commit()
        result = 'success'
        return result

    elif user_byID is None:
        result = 'nk_duplicated'
        return  result

    else:
        result = 'id_duplicated'
        return result

def user_login(userID, password):
    bytes_password = password.encode('utf-8')


    user_byID = userDB.query.filter(userID == userDB.user_id).first()
    if user_byID:
        if bcrypt.checkpw(bytes_password, user_byID.user_pw.encode('utf-8')):
            return True
    else :
        False

def get_query_by_pk(id):
    query_pk = models.video_info.query.filter(id == models.video_info.id).first()
    return query_pk
    
def get_nick(userID):
    user_byID = userDB.query.filter(userID == userDB.user_id).first()
    nick = user_byID.user_nick
    return nick

def get_profile(userID):
    userID = userDB.query.filter(userID == userDB.user_id).first()
    profile = userID.user_prof
    return profile
        
def path_by_local(category, video_title, video_duration, youtube_url ,s3_title, video_path, audio_path):
    new_file = models.video_info(category=category, video_title=video_title, video_duration = video_duration, youtube_url=youtube_url,s3_title=s3_title, s3_video=video_path, s3_audio=audio_path)
    db.session.add(new_file)
    db.session.commit()
    by_title = models.video_info.query.filter(s3_title == models.video_info.s3_title).order_by(models.video_info.id.desc()).first()
    id = by_title.id
    return id

def get_video_info(video_id):
    by_id = models.video_info.query.filter(video_id == models.video_info.id).order_by(models.video_info.id.desc()).first()
    title = by_id.video_title
    path = by_id.s3_video
    duration = by_id.video_duration
    return title, path, duration

def find_duplicatuon(video_title):
    by_title = models.video_info.query.filter(video_title == models.video_info.video_title).order_by(models.video_info.id.desc()).first()
    id = by_title.id
    return id

def find_path(video_pk):
    by_id = models.video_info.query.filter(video_pk == models.video_info.id).order_by(models.video_info.id.desc()).first()
    audio_path = by_id.s3_audio
    video_path = by_id.video_path
    return video_path, audio_path
