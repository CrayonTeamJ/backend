from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, sql
import uuid


class user_info(db.Model):
    __tablename__='user_info'
    user_pk = db.Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(150), unique=True, nullable=False)
    user_pw = db.Column(db.String(200), nullable=False)
    user_nick = db.Column(db.String(120), unique=True, nullable=False)
    user_prof = db.Column(db.Text, nullable=True, default = 'default value')

    def __init__(self, user_id, user_pw, user_nick):
        self.user_id=user_id
        self.user_pw=user_pw
        self.user_nick=user_nick