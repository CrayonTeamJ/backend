from models import user_info
from operator import ne
import sys, os
from sqlalchemy import sql, func, select
from sqlalchemy.sql.expression import false
os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
import models
from app import app, db
import bcrypt


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
        

