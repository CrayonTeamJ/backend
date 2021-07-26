from app import db
from enum import unique
from sqlalchemy.sql.schema import Sequence
from sqlalchemy.sql.sqltypes import Integer
from flask_sqlalchemy import SQLAlchemy
#from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, sql
import uuid



class user_info(db.Model):
    __tablename__='user_info'
    id = db.Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(150), unique=True, nullable=False)
    user_pw = db.Column(db.String(200), nullable=False)
    user_nick = db.Column(db.String(120), unique=True, nullable=False)
    user_prof = db.Column(db.Text, nullable=True, default = 'https://crayon-team-j.s3.ap-northeast-2.amazonaws.com/sample_image.jpeg')

    def __init__(self, user_id, user_pw, user_nick):
        self.user_id=user_id
        self.user_pw=user_pw
        self.user_nick=user_nick

class video_info(db.Model):
    __tablename__="video_info"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.Boolean, nullable=False)
    video_title = db.Column(db.String(150))
    video_duration = db.Column(db.String(150))
    s3_title = db.Column(db.String(150))
    youtube_url = db.Column(db.String(150))
    s3_video = db.Column(db.String(150))
    s3_audio = db.Column(db.String(150))
    
    def __init__(self, category, video_title, video_duration, s3_title, s3_video, s3_audio):
        self.category = category
        self.video_title = video_title
        self.video_duration = video_duration
        self.s3_title = s3_title
        self.s3_video = s3_video
        self.s3_audio = s3_audio


class image_info(db.Model):
    __tablename__="image_info"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    video_pk = db.Column(db.Integer, ForeignKey('video_info.id'))
    s3_path = db.Column(db.String(150), unique=True)
    time_reccord = db.Column(db.String(150))

    def __init__(self, video_pk, s3_path):
        self.video_pk = video_pk
        self.s3_path = s3_path
