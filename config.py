import os

BASE_DIR = os.path.dirname(__file__)

JWT_SECRET_KEY = "I'M IML"
SECRET_KEY ='Thisissupportedtobesecret!'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dbmasteruser:password@ls-6903eff556ee7c5df46a43f5f8d4d3025d35276f.cxbztv2km60w.ap-northeast-2.rds.amazonaws.com/USERinfo'.format(os.path.join(BASE_DIR, 'app.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False