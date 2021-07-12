from flask import Flask, redirect, render_template, url_for, jsonify, Response, make_response, request
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import insert, true
from werkzeug.wrappers import response
import logging
import config


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate() 
CORS(app) # 있어야 프런트와 통신 가능, 없으면 오류뜸

  
app.config.from_object(config)
db.init_app(app)
migrate.init_app(app, db)

from models import user_info
import views

logging.basicConfig(level=logging.DEBUG )



@app.route('/api')
def index():
    print("hello world")
    app.logger.info('hello world - app logger ') 
    return Response("test", status=201, mimetype='text/html')
    #return make_response(jsonify({'success' : 'success'}), 200)

@app.route('/api/signup', methods=['GET'])
def hello():
  
    return "Login Page"




@app.route('/api/login', methods=['POST'])
def login():
    userform = request.json
    views.user_login(userform['userID'], userform['password'])
    if True:
        return "LogIn Success"
            
    else:
        return '<h1>Invalid username of password</h1>'

    
@app.route('/api/signup', methods=['POST'])

def signup():
    userform = request.json
    views.user_insert(userform['userID'], userform['password'], userform['nickname'])
        
    if 'id_duplicated':
        return make_response(jsonify({'Result' : 'ID_duplicated'}), 400)
    
    elif 'nk_duplicated':
        return make_response(jsonify({'Result' : 'NK_duplicated'}), 201)

    else:
        return {'Result' : 'Success'}




if __name__ == '__main__':
    app.run(debug=True) 