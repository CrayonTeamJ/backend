import os

BASE_DIR = os.path.dirname(__file__)

JWT_SECRET_KEY = "I'M IML"
SECRET_KEY ='Thisissupportedtobesecret!'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dbmasteruser:password@ls-d8e66d0492f2c70ce3ecd3e603cf642a8c8a8351.cqobb3tz8sun.ap-northeast-2.rds.amazonaws.com/USERinfo'.format(os.path.join(BASE_DIR, 'app.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False