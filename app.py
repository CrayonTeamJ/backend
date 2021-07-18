import views
import os
from flask import Flask, jsonify, Response, make_response, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_jwt_extended import *
import logging
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
import config
from function.video_func import *
from function.s3_control import *

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
CORS(app, supports_credentials=True)  # 있어야 프런트와 통신 가능, 없으면 오류뜸
jwt = JWTManager(app)

JWT_COOKIE_SECURE = False  # https를 통해서만 cookie가 갈 수 있는지 (production 에선 True)
app.config["JWT_TOKEN_LOCATION"] = [
    'cookies', "headers", "json"]  # 토큰을 어디서 찾을지에 대한 내용
JWT_COOKIE_CSRF_PROTECT = True
JWT_ACCESS_TOKEN_EXPIRES = 600000

app.config.from_object(config)
db.init_app(app)
migrate.init_app(app, db)

logging.basicConfig(level=logging.DEBUG)
file_number = 0


@app.route('/api/input', methods=['GET'])
@jwt_required(optional=True)
def user_only():
    cur_user = get_jwt_identity()
    if cur_user is None:
        return make_response(jsonify({'Result': 'Fail', 'message': 'Not_user'}), 203)
    else:
        return make_response(jsonify({'Result': 'Success', 'message': 'Is_user'}), 200)



@app.route('/api/videoUpload', methods=['POST'])
def video_input():
    global file_number

    if request.form['video_type'] == "1":
        Your_input = request.files['file']
        video_filename = 'video' + str(file_number) + '.mp4'
        # video_filename=secure_filename(Your_input.filename)
        file_path = os.path.join('./data/', video_filename)
        Your_input.save(file_path)
        mp4_to_mp3(file_path, file_number)
        upload_blob_file(file_path, 'video/video' + str(file_number) + '.mp4')
        upload_blob_file('./data/audio' + str(file_number) +
                         '.mp3', 'audio/audio' + str(file_number) + '.mp3')
        video_path = 'https://teamj-data.s3.ap-northeast-2.amazonaws.com/video/' + video_filename
        audio_path = 'https://teamj-data.s3.ap-northeast-2.amazonaws.com/audio/audio' + \
            str(file_number) + '.mp3'
        os.remove('./data/'+video_filename)
        os.remove('./data/audio' + str(file_number) + '.mp3')
        video_pk = views.path_by_local(
            False, video_filename, video_path, audio_path)
        file_number += 1
        return make_response(jsonify({'Result': 'Success'}, {'video_pk': video_pk}), 200)

    elif request.form['video_type'] == "0":
        Your_input = request.form['video_url']
        video_filename = 'video' + str(file_number) + '.mp4'
        download_video(Your_input, file_number)
        upload_blob_file('./data/video' + str(file_number) +
                         '.mp4', 'video/video' + str(file_number) + '.mp4')

        download_audio(Your_input, file_number)
        upload_blob_file('./data/audio' + str(file_number) +
                         '.mp3', 'audio/audio' + str(file_number) + '.mp3')
        video_path = 'https://teamj-data.s3.ap-northeast-2.amazonaws.com/video/' + video_filename
        audio_path = 'https://teamj-data.s3.ap-northeast-2.amazonaws.com/audio/audio' + \
            str(file_number) + '.mp3'
        os.remove('./data/video' + str(file_number) + '.mp4')
        os.remove('./data/audio' + str(file_number) + '.mp3')

        video_pk = views.path_by_local(
            False, video_filename, video_path, audio_path)

        file_number += 1
        return make_response(jsonify({'Result': 'Success'}, {'video_pk': video_pk}), 200)

@app.route('/api/refresh', methods=['GET'])
@jwt_required(refresh=True, optional=True)  # @jwt_required(locations="headers")
def refresh():
    current_user = get_jwt_identity()
    if current_user is None:
        return make_response(jsonify({'Result': 'fail', 'message': 'Not_user'}), 203)

    else:
        access_token = create_access_token(identity=current_user)
        return jsonify(Result='success', access_token=access_token, current_user=current_user, access_expire=JWT_ACCESS_TOKEN_EXPIRES), 200

@app.route('/api/logout', methods=['GET'])
def logout():
    # current_user = get_jwt_identity()
    access_token = "no"
    resp = jsonify(Result="success", access_token=access_token,
                   access_expire=0, isLogin=False)
    return resp, 200

@app.route('/api/login', methods=['POST'])
def login():
    userform = request.json
    UserLogin = views.user_login(userform['userID'], userform['password'])

    if UserLogin == True:
        refresh_token = create_refresh_token(identity=userform['userID'])
        nick = views.get_nick(userform['userID'])
        profile = views.get_profile(userform['userID'])

        resp = jsonify(Result='success', access_expire=JWT_ACCESS_TOKEN_EXPIRES, access_token=create_access_token(identity=userform['userID']),
                       Nickname=nick, Profile=profile, isLogin=True)
        #set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200

        # return make_response(jsonify(Result = "success", access_token = create_access_token(identity = userform['userID'], expires_delta = False)))
        # return make_response(jsonify({'Result' : 'Login_Success',}, access_token = create_access_token(identity = userform['userID'], expires_delta = False)))

    else:
        return make_response(jsonify({'Result': 'fail'}), 203)

@app.route('/api/signup', methods=['POST'])
def signup():
    userform = request.json
    dup_test = views.user_insert(
        userform['userID'], userform['password'], userform['nickname'])

    if dup_test == 'id_duplicated':
        return make_response(jsonify({'Result': 'ID_duplicated'}), 202)

    elif dup_test == 'nk_duplicated':
        return make_response(jsonify({'Result': 'NK_duplicated'}), 203)

    else:
        return make_response(jsonify({'Result': 'Success'}), 200)

if __name__ == '__main__':
    app.run(debug=True)