import os
from flask import Flask, jsonify, Response, make_response, request, json, redirect
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
from function.clova_func import *
from function.trans import *
from flask_celery import make_celery
import requests
from pytube import YouTube
from flask_pymongo import PyMongo
import views
import time
# from elasticsearch import Elasticsearch



app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
CORS(app, supports_credentials=True)  # 있어야 프런트와 통신 가능, 없으면 오류뜸
jwt = JWTManager(app)
celery = make_celery(app)

# this is only about mongodb
app.config["MONGO_URI"] = "mongodb+srv://Crayon:pc2Af0vKZWbkT7GL@clustercrayon.lij0j.mongodb.net/voicedb?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
coll = mongodb_client.db.voice_files_list


def save_audio_result_to_mongo(video_pk, post_result):
    coll.insert({
        'video_number': video_pk,
        'sentence_list': post_result['sentence_list']
    })


def clova(audio_path, lang):
    pre_result = ClovaSpeechClient().req_url(url=audio_path, language = lang, completion='sync')
        # print('type_of_preresult:', type(pre_result))
    
    post_result = to_json(pre_result)
        # print('type_of_postresult:', type(post_result))
    

    return post_result


#task
import tasks
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
video_pk_g = 0


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
    global video_pk_g

    lang = request.form['language']

    file_number_inside = file_number
    file_number += 1

    # audio_path = 0
    # video_pk = 0

    if request.form['video_type'] == "1":
        Your_input = request.files['file']
        # print('Your_input: ', Your_input)
        # print('=====================')
        video_filename = 'video' + str(file_number_inside) + '.mp4'
        # print('video_filename: ', video_filename)
        # print('======================')
        # video_filename=secure_filename(Your_input.filename)
        file_path = os.path.join('./data/', video_filename)
        Your_input.save(file_path)
        mp4_to_mp3(file_path, file_number_inside)
        # 클로바 실행시 아래 두 줄 주석 취소하기
        # upload_blob_file(file_path, 'video/video' + str(file_number_inside) + '.mp4')
        # upload_blob_file('./data/audio' + str(file_number_inside) +
                        #  '.mp3', 'audio/audio' + str(file_number_inside) + '.mp3')
        video_path = 'https://teamj-data.s3.ap-northeast-2.amazonaws.com/video/' + video_filename
        audio_path = 'https://teamj-data.s3.ap-northeast-2.amazonaws.com/audio/audio' + \
            str(file_number_inside) + '.mp3'
        os.remove('./data/'+video_filename)
        os.remove('./data/audio' + str(file_number_inside) + '.mp3')
        video_pk = views.path_by_local(
            False, video_filename, video_path, audio_path)
        video_pk_g = video_pk
        
        post_result = clova(audio_path, lang)
        #send result to model server
        send_to_yolo(video_path, video_pk)
        save_audio_result_to_mongo(video_pk, post_result)

        return make_response(jsonify({'Result': 'Success', 'video_pk': video_pk}), 200)

    elif request.form['video_type'] == "0":
        # print(file_number_inside)
        Your_input = request.form['video_url']
        validate = url_valid(Your_input)
        if validate == False:
            return make_response(jsonify({'Result': 'false'}), 202)

        video_filename = 'video' + str(file_number_inside) + '.mp4'
        # 클로바 실행시 아래 두 줄 주석 취소하기
        video_info = tasks.async_download_video(Your_input, file_number_inside)
        upload_blob_file('./data/video' + str(file_number_inside) +
                         '.mp4', 'video/video' + str(file_number_inside) + '.mp4')
        video_duration = video_info[0]
        video_title = video_info[1]

        # 클로바 실행시 아래 두 줄 주석 취소하기
        tasks.async_download_audio(Your_input, file_number_inside)

        upload_blob_file('./data/audio' + str(file_number_inside) +
                         '.mp3', 'audio/audio' + str(file_number_inside) + '.mp3')
        video_path = 'https://teamj-data.s3.ap-northeast-2.amazonaws.com/video/' + video_filename
        audio_path = 'https://teamj-data.s3.ap-northeast-2.amazonaws.com/audio/audio' + str(file_number_inside) + '.mp3'
        os.remove('./data/video' + str(file_number_inside) + '.mp4')
        os.remove('./data/audio' + str(file_number_inside) + '.mp3')

        video_pk = views.path_by_local(
            True, video_filename, video_path, audio_path)
        
        # send result to model server
        send_to_yolo(video_path, video_pk)

        post_result = clova(audio_path, lang)
        save_audio_result_to_mongo(video_pk, post_result)

        return make_response(jsonify({'Result': 'Success', 'video_pk': video_pk}), 200)


@app.route('/api/refresh', methods=['GET'])
# @jwt_required(locations="headers")
@jwt_required(refresh=True, optional=True)
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
        set_refresh_cookies(resp, refresh_token)
        return resp, 200

        return make_response(jsonify(Result = "success", access_token = create_access_token(identity = userform['userID'], expires_delta = False)))
        return make_response(jsonify({'Result' : 'Login_Success',}, access_token = create_access_token(identity = userform['userID'], expires_delta = False)))

    else:
        return make_response(jsonify({'Result': 'fail'}), 203)


@app.route('/api/signup', methods=['POST'])
def signup():
    userform = request.json
    dup_test = tasks.async_user_insert(
        userform['userID'], userform['password'], userform['nickname'])

    if dup_test == 'id_duplicated':
        return make_response(jsonify({'Result': 'ID_duplicated'}), 202)

    elif dup_test == 'nk_duplicated':
        return make_response(jsonify({'Result': 'NK_duplicated'}), 203)

    else:
        return make_response(jsonify({'Result': 'Success'}), 200)


# @app.route("/to_yolo")
# def dataToYolo():
#     # 뭘 보내야 하나요 비디오 pk, 비디오 링크
#     video_pk = 16
#     line = views.get_query_by_pk(video_pk)
#     pk = line.video_pk
#     video_path = line.s3_video
#     data = {'video_pk': pk, 's3_video': video_path}
#     return requests.post('http://0.0.0.0:5001/to_yolo', json=data).content

def send_to_yolo(video_path, video_pk):
    data = {"video_path": video_path, "video_pk": video_pk}
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://localhost:5050/to_yolo', headers=headers, data=data, verify=False)
    if response.ok:
        pass
    else:
        print(response.json())
    # return requests.post('http://localhost:5001/to_yolo', json=data).content


@app.route('/api/search', methods=['GET'])
def search():

    # print(request.args.to_dict())
    req_query= request.args.to_dict()
    searchaud= req_query['searchaud']
    # searchvid= req_query['searchvid']
    searchtype= req_query['searchtype']
    video_id= req_query['id']
    

#     if searchtype == 'image':
#         #image search

#     elif searchtype == 'audio':

#         es = Elasticsearch('http://elasticsearch:9200')
        
#         #mongo db에서 가져오기(index)
#         # index = [검색할_인덱스]
#         # query_body = [검색할_쿼리문]
        

#         res = es.search(index='voicedb.voice_files_list', body=query_body)
#         # res에 검색 결과가 담겨져 있다

    return make_response(request.args.to_dict(), 200)



# "GET /api/search?searchaud=인물검색&searchtype=1 HTTP/1.1"


if __name__ == '__main__':
    app.run(debug=True)
