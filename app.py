import sys, os
from flask import Flask, redirect, render_template, url_for, jsonify, Response, make_response, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_jwt_extended import *
import logging
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
import config

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate() 
CORS(app) # 있어야 프런트와 통신 가능, 없으면 오류뜸
jwt = JWTManager(app)

JWT_COOKIE_SECURE = False # https를 통해서만 cookie가 갈 수 있는지 (production 에선 True)
app.config["JWT_TOKEN_LOCATION"] = ['cookies', "headers", "json"] #토큰을 어디서 찾을지에 대한 내용
JWT_COOKIE_CSRF_PROTECT = True 
JWT_ACCESS_TOKEN_EXPIRES = 300000

app.config.from_object(config)
db.init_app(app)
migrate.init_app(app, db)

import views

logging.basicConfig(level=logging.DEBUG )


@app.route('/api/input', methods=['GET'])
@jwt_required()
def user_only():
	cur_user = get_jwt_identity()
	if cur_user is None:
		return make_response(jsonify({'Result' : 'Fail', 'message' : 'Not_user'}), 203)
	else:
		return make_response(jsonify({'Result' : 'Success', 'message' : 'Is_user'}), 200)

@app.route('/api/input', methods=['POST'])
def video_input():

    if request.form['image_type'] == "1" :
        Your_input = request.files['file']
        video_filename=secure_filename(Your_input.filename)
        Your_input.save(os.path.join('./data/',video_filename))
        return make_response(jsonify({'Result' : 'Success'}), 200)

        # gcp_control.upload_blob_filename('teamg-data','./data/'+video_filename,video_filename)
        # video_path = 'https://storage.googleapis.com/teamg-data/'+video_filename
        # video_path_signed = gcp_control.generate_download_signed_url_v4('teamg-data', video_filename)
        # os.remove('./data/'+video_filename)
        # views.video_insert('local',video_filename,video_path_signed)

@app.route('/api/refresh', methods=['GET'])
@jwt_required(refresh=True) #@jwt_required(locations="headers")
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token, current_user=current_user, access_expire = JWT_ACCESS_TOKEN_EXPIRES)



@app.route('/api/login', methods=['POST'])
def login():
    userform = request.json
    UserLogin = views.user_login(userform['userID'], userform['password'])
    
    if UserLogin == True:
        access_token = create_access_token(identity=userform['userID'])
        refresh_token = create_refresh_token(identity=userform['userID'])

        resp = jsonify(Result = 'success', access_expire = JWT_ACCESS_TOKEN_EXPIRES, access_token = create_access_token(identity = userform['userID']))
        #set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200
        
        #return make_response(jsonify(Result = "success", access_token = create_access_token(identity = userform['userID'], expires_delta = False)))
        #return make_response(jsonify({'Result' : 'Login_Success',}, access_token = create_access_token(identity = userform['userID'], expires_delta = False)))
            
    else:
        return make_response(jsonify({'Result' : 'fail'}), 203)

    
@app.route('/api/signup', methods=['POST'])

def signup():
    userform = request.json
    dup_test = views.user_insert(userform['userID'], userform['password'], userform['nickname'])
        
    if dup_test == 'id_duplicated':
        return make_response(jsonify({'Result' : 'ID_duplicated'}), 202)
    
    elif dup_test == 'nk_duplicated':
        return make_response(jsonify({'Result' : 'NK_duplicated'}), 203)

    else:
        return make_response(jsonify({'Result' : 'Success'}), 200)




if __name__ == '__main__':
    app.run(debug=True) 