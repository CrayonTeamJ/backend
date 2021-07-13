import sys, os
from flask import Flask, redirect, render_template, url_for, jsonify, Response, make_response, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
import logging
from werkzeug.utils import secure_filename
import config

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate() 
CORS(app) # 있어야 프런트와 통신 가능, 없으면 오류뜸
jwt = JWTManager(app)

app.config.from_object(config)
db.init_app(app)
migrate.init_app(app, db)

import views

logging.basicConfig(level=logging.DEBUG )
#

@app.route('/api/login', methods=['POST'])
def login():
    userform = request.json
    UserLogin = views.user_login(userform['userID'], userform['password'])
    
    if UserLogin == True:
        return make_response(jsonify(Result = "success", access_token = create_access_token(identity = userform['userID'], expires_delta = False)))
        #return make_response(jsonify({'Result' : 'Login_Success',}, access_token = create_access_token(identity = userform['userID'], expires_delta = False)))
            
    else:
        return make_response(jsonify({'Result' : 'Login_Fail'}), 203)

    
@app.route('/api/signup', methods=['POST'])

def signup():
    userform = request.json
    dup_test = views.user_insert(userform['userID'], userform['password'], userform['nickname'])
        
    if dup_test == 'id_duplicated':
        return make_response(jsonify({'Result' : 'ID_duplicated'}), 203)
    
    elif dup_test == 'nk_duplicated':
        return make_response(jsonify({'Result' : 'NK_duplicated'}), 203)

    else:
        return make_response(jsonify({'Result' : 'Success'}), 200)




if __name__ == '__main__':
    app.run(debug=True) 