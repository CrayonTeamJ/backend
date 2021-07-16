from operator import ne
import sys, os
from sqlalchemy import sql, func, select
from sqlalchemy.sql.expression import false
os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
import models
#from app import app, db
import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
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
    
def get_nick(userID):
    user_byID = userDB.query.filter(userID == userDB.user_id).first()
    nick = user_byID.user_nick
    return nick

def get_profile(userID):
    userID = userDB.querry.filter(userID == userDB.user_id).first()
    profile = userID.user_prof
    return profile
        
def path_by_local(category, title, video_path, audio_path):
    new_file = models.video_info(category=category, title=title, s3_video=video_path, s3_audio=audio_path)
    db.session.add(new_file)
    db.session.commit()
    by_title = models.video_info.query.filter(title == models.video_info.title).first()
    video_pk = by_title.video_pk
    return video_pk

