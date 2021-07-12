from models import user_info
from operator import ne
import sys, os
from sqlalchemy import sql, func, select
from sqlalchemy.sql.expression import false
os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
import models
from app import app, db

user = models.user_info


def user_insert(userID, userPW, userNICK):
    user_byID = user.query.filter(userID == user.user_id).first()
    user_byNK = user.query.filter(userNICK == user.user_nick).first()
    
    if user_byID is None and user_byNK is None:
        new_user = user(userID, userPW, userNICK)
        db.session.add(new_user)
        db.session.commit()
        result = 'success'
        return result

    elif (userID == user_byID.user_id) or (user_byID is None):
        result = 'id_duplicated'
        return  result

    elif userNICK == user_byNK.user_nick:
        result = 'nk_duplicated'
        return result
    
    
        

def user_login(userID, password):

    user = models.user_info.query.filter(userID == models.user_info.user_id).first()
    if user:
        if user.user_pw == password:
            return True
        

