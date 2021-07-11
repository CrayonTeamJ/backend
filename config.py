import os

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY ='Thisissupportedtobesecret!'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://아이디:패스워드@ls-d8e66d0492f2c70ce3ecd3e603cf642a8c8a8351.cqobb3tz8sun.ap-northeast-2.rds.amazonaws.com/USERinfo'.format(os.path.join(BASE_DIR, 'app.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False