from app import db

class user_info(db.Model):
    __tablename__='user_info'
    user_sn = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(150), unique=True, nullable=False)
    user_pw = db.Column(db.String(200), nullable=False)
    user_nick = db.Column(db.String(120), unique=True, nullable=False)
    user_prof = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, user_pw, user_nick, user_prof):
        self.user_id=user_id
        self.user_pw=user_pw
        self.user_nick=user_nick
        self.user_prof=user_prof