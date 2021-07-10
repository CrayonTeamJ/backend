from operator import ne
import sys, os
from sqlalchemy import sql, func
os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
import models
from app import app, db


def user_insert(user_id, user_pw, user_nick):
    new_user = models.user_info(user_id, user_pw, user_nick)
    db.session.add(new_user)
    db.session.commit()
