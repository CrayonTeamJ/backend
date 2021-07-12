from models import user_info
from operator import ne
import sys, os
from sqlalchemy import sql, func, select
from sqlalchemy.sql.expression import false
os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
import models
from app import app, db


def user_insert(user_id, user_pw, user_nick):
    reuslt = 'false'
    Find_dupe_id = select(user_info).where(user_id == user_info.user_id)
    Find_dupe_nk = select(user_info).where(user_pw == user_info.user_nick)
    user = models.user_info.query.filter(user_id == models.user_info.user_id).first()
    

    if user_id != Find_dupe_id:
        result = 'id_duplicated'
        return  result

    elif Find_dupe_nk == True:
        result = 'nk_duplicated'
        return result
    
    else :
        new_user = models.user_info(user_id, user_pw, user_nick)
        db.session.add(new_user)
        db.session.commit()
        result = 'success'
        return result

def user_login(userID, password):

    user = models.user_info.query.filter(userID == models.user_info.user_id).first()
    if user:
        if user.user_pw == password:
            return True
        

