
import os
import celery
from flask import Flask, jsonify, Response, make_response, request, json, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_jwt_extended import *
import logging
from pymongo.common import validate_ok_for_update
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
import config
from function.video_func import *
from function.s3_control import *
from function.clova_func import *
from function.trans import *
from celery import Celery
import requests
from pytube import YouTube
from flask_pymongo import PyMongo
import asyncio
import time

import time
import function
from elasticsearch import Elasticsearch


app = Flask(__name__)
app.config['JSON_SORT_KEYS']=False
db = SQLAlchemy()
migrate = Migrate()
CORS(app, supports_credentials=True)  # 있어야 프런트와 통신 가능, 없으면 오류뜸
jwt = JWTManager(app)
def make_celery(app):
    celery = Celery(
        'tasks',
        backend= 'amqp://admin:mypass@rabbit:5672/',
        broker= 'amqp://admin:mypass@rabbit:5672/', include=["tasks"]
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

simple_tasks = make_celery(app)
import views
# this is only about mongodb
app.config["MONGO_URI"] = os.environ['MONGO_URI_env']
mongodb_client = PyMongo(app)
coll = mongodb_client.db.voice_files_list
coll2 = mongodb_client.db.video_files_list
coll3 = mongodb_client.db.images_coll


#task
import tasks
JWT_COOKIE_SECURE = False  # https를 통해서만 cookie가 갈 수 있는지 (production 에선 True)
app.config["JWT_TOKEN_LOCATION"] = [
    'cookies', "headers", "json"]  # 토큰을 어디서 찾을지에 대한 내용
JWT_COOKIE_CSRF_PROTECT = True
JWT_ACCESS_TOKEN_EXPIRES = 6000000

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
        video_filename = 'video' + str(file_number_inside) + '.mp4'
        #이미 DB에 저장되어있으면 패스
        video_title = request.files['file'].filename
        try: 
            views.find_duplicatuon(video_title)
            id = views.find_duplicatuon(video_title)
            return make_response(jsonify({'Result': 'Success', 'video_pk': id, 'yolo_id' : 'duplicate', 'clova_id' : 'duplicate' }), 200)
        except:
            # video_filename=secure_filename(Your_input.filename)
            file_path = os.path.join('./data/', video_filename)
            Your_input.save(file_path)
            video_duration = vid_duration(file_path)
            mp4_to_mp3(file_path, file_number_inside)
           
            upload_blob_file(file_path, 'video/video' + str(file_number_inside) + '.mp4')
            upload_blob_file('./data/audio' + str(file_number_inside) +
                            '.mp3', 'audio/audio' + str(file_number_inside) + '.mp3')
            video_path = 'https://crayon-team-j.s3.ap-northeast-2.amazonaws.com/video/' + video_filename
            audio_path = 'https://crayon-team-j.s3.ap-northeast-2.amazonaws.com/audio/audio' + str(file_number_inside) + '.mp3'
            os.remove('./data/'+video_filename)
            os.remove('./data/audio' + str(file_number_inside) + '.mp3')
            video_pk = views.path_by_local(False, video_title, video_duration, video_path, video_filename,video_path, audio_path)

            Clova = simple_tasks.send_task('tasks.run_clova', kwargs={'video_pk' : video_pk, 'audio_path' : audio_path, 'lang': lang})
            
            app.logger.info("Invoking Method ")
            YOLO = simple_tasks.send_task('tasks.sendto_yolo', kwargs={'video_path': video_path, 'video_pk' : video_pk})
            app.logger.info(YOLO.backend)
            

            return make_response(jsonify({'Result': 'Success', 'video_pk': video_pk, 'yolo_id' : YOLO.id, 'clova_id' : Clova.id}), 200)

    elif request.form['video_type'] == "0":
        # print(file_number_inside)
        Your_input = request.form['video_url']
        validate = url_valid(Your_input)
        if validate == False:
            return make_response(jsonify({'Result': 'false', 'yolo_id' : 'duplicate', 'clova_id' : 'duplicate'}), 202)
        video_title = get_youtube_title(Your_input)

        try: 
            views.find_duplicatuon(video_title)
            id = views.find_duplicatuon(video_title)
            return make_response(jsonify({'Result': 'Success', 'video_pk': id, 'yolo_id' : 'duplicate', 'clova_id' : 'duplicate'}), 200)
        except:

            video_filename = 'video' + str(file_number_inside) + '.mp4'
            #video_duration = download_video(Your_input, file_number_inside)

            video_duration = asyncio.run(download_both(Your_input, file_number_inside))
            upload_blob_file('./data/video' + str(file_number_inside) +
                            '.mp4', 'video/video' + str(file_number_inside) + '.mp4')
            upload_blob_file('./data/audio' + str(file_number_inside) +
                            '.mp3', 'audio/audio' + str(file_number_inside) + '.mp3')
            video_path = 'https://crayon-team-j.s3.ap-northeast-2.amazonaws.com/video/' + video_filename
            audio_path = 'https://crayon-team-j.s3.ap-northeast-2.amazonaws.com/audio/audio' + str(file_number_inside) + '.mp3'
            os.remove('./data/video' + str(file_number_inside) + '.mp4')
            os.remove('./data/audio' + str(file_number_inside) + '.mp3')

            video_pk = views.path_by_local(
                True, video_title, video_duration , Your_input, video_filename,  video_path, audio_path)
            Clova = simple_tasks.send_task('tasks.run_clova', kwargs={'video_pk' : video_pk, 'audio_path' : audio_path, 'lang': lang})

            app.logger.info("Invoking Method ")
            YOLO = simple_tasks.send_task('tasks.sendto_yolo', kwargs={'video_path': video_path, 'video_pk' : video_pk})
            time.sleep(3)
            app.logger.info(YOLO.id)
            app.logger.info(Clova.id)
            

            return make_response(jsonify({'Result': 'Success', 'video_pk': video_pk, 'yolo_id' : YOLO.id, 'clova_id' : Clova.id}), 200)


@app.route('/api/apiStatus', methods=['POST'])
async def reply():
    task_id = request.json
    yolo_id = task_id['yolo_id']
    clova_id = task_id['clova_id']
    app.logger.info(request.json)
    for _ in range(1000):
        clova_result = "fail"
        if simple_tasks.AsyncResult(clova_id).successful() == True:
            clova_result = "Success"
            break
        await asyncio.sleep(0.3)
        

    app.logger.info(clova_result)
    for _ in range(1000):
        yolo_result = "fail"
        if simple_tasks.AsyncResult(yolo_id).successful() == True:
            yolo_result = 'Success'
            break
        await asyncio.sleep(0.3)
    app.logger.info(yolo_result)
    return make_response(jsonify({'yolo_res': yolo_result, 'clova_res': clova_result}), 200)


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


def send_to_yolo(video_path, video_pk):
    data = {"video_path": video_path, "video_pk": video_pk}
    response = requests.post('http://backend_model:5050/to_yolo', json=data, verify=False)


from aud_search import *
from time import sleep

@app.route('/api/audiosearch', methods=['GET'])
def audiosearch():

    video_id = int(request.args.get('id'))
    keyword = request.args.get('search_aud')

    videos = views.get_video_info(video_id)
    title, url, duration = videos[0], videos[1], videos[2]
    search_info_aud = {'search_aud': keyword, 'type': "audio", 'search_vid' : ''}
    vid_info = {'title': title, 's3_url': url, 'video_length': duration}

    try:
        deleteIndex()
        createIndex()

        for s in coll.find({"video_number":video_id}):
            sentence_list = s['sentence_list']
            for key in sentence_list:
                input_elastic = {'video_number': video_id, 'sentence': key['sentence'], 'start_time': key['start_time']}
                insert_data(input_elastic)

        sleep(1)

        res = audio_search(video_id, keyword)

        hit1 = res['hits']
        hit2 = hit1['hits']

        if not hit2:
            return jsonify({'result': "success", 'video_info': vid_info, 'search_info': search_info_aud, 'res_info': hit2})

        time=[]
        for key in hit2:
            source = key['_source']
            time.append(source['start_time'])

        time_and_path = []
        for s in coll3.find({"video_pk":video_id}):
            image_list = s['image_list']
            for key in image_list:
                time_and_path.append([key['time'], key['path']])

        result_list=[]
        for i in time_and_path:
            for j in time:
                start = round(j/1000)
                if start == i[0]:
                    result_list.append({'start':i[0], 'thumbnail':i[1]})

        return jsonify({'result': "success", 'video_info': vid_info, 'search_info': search_info_aud, 'res_info': result_list})

    except:
        return jsonify({'result': "fail", 'video_info': vid_info, 'search_info': search_info_aud })


# @app.route('/api/audiosearch2', methods=['GET'])
# def search():

#     video_id = int(request.args.get('id'))
#     keyword = request.args.get('search_aud')

#     videos = views.get_video_info(video_id)
#     title, url, duration = videos[0], videos[1], videos[2]
#     search_info = {'search_aud': keyword, 'type': "audio"}

#     try:
#         sentence_list = []
#         for s in coll.find({"video_number":video_id}):
#             sentence_list.append(s['sentence_list'])

#         start = []
#         for i in range(len(sentence_list[0])):
#             if keyword in sentence_list[0][i]['sentence']:
#                 start.append([round(sentence_list[0][i]['start_time']/1000)])

#         time_and_path = []
#         for s in coll3.find({"video_pk":video_id}):
#             image_list = s['image_list']
#             for key in image_list:
#                 time_and_path.append([key['time'], key['path']])


#         start_and_path = []
#         for i in range(len(start)):
#             for j in range(len(time_and_path)):
#                 if start[i][0] == time_and_path[j][0]:
#                     start_and_path.append([start[i][0], time_and_path[j][1]])


#         result_list = []
#         for i in start_and_path:
#             dictionary = {'start': i[0], 'thumbnail': i[-1]}
#             dictionary_copy = dictionary.copy()
#             result_list.append(dictionary_copy)


#         vid_info = {'title': title, 'video_length': duration, 's3_url': url}
#         return jsonify({'result': "success", 'video_info': vid_info, 'search_info': search_info, 'res_info': result_list})
    
#     except:
#         vid_info2 = {'title': title, 's3_url': url, 'video_length': duration}
#         return jsonify({'result': "fail", 'video_info': vid_info2})


from img_search import *

@app.route('/api/videosearch', methods=['GET'])
def videosearch():

    video_id = int(request.args.get('id'))
    keyword = request.args.get('search_img')

    total_len = 0
    videos = views.get_video_info(video_id)
    title, url, duration = videos[0], videos[1], videos[2]
    search_info = {'search_vid': keyword, 'type': "video", 'search_aud' : ''}

    try:
        detected_seconds = image_search(video_id, keyword)
        if not detected_seconds:
            vid_info = {'title': title, 'video_length': duration, 'length':total_len, 's3_url': url}
            return jsonify({'result': "success", 'video_info': vid_info, 'search_info': search_info, 'res_info': detected_seconds}) 

        start_and_end = groupSequence(detected_seconds)

        path_and_time = []
        for s in coll3.find({"video_pk":video_id}):
            image_list = s['image_list']
            for key in image_list:
                path_and_time.append([key['time'], key['path']])

        start_and_end_and_path = []
        for i in range(len(start_and_end)):
            for j in range(len(path_and_time)):
                if start_and_end[i][0] == path_and_time[j][0]:
                    start_and_end_and_path.append([start_and_end[i][0], start_and_end[i][-1], path_and_time[j][-1]])

        result_list = []
        for i in start_and_end_and_path:
            total_len += (i[1]-i[0])
            dictionary = {'start': i[0], 'end': i[1], 'leng': i[1]-i[0], 'thumbnail': i[-1]}
            dictionary_copy = dictionary.copy()
            result_list.append(dictionary_copy)

        vid_info = {'title': title, 'video_length': duration, 'length':total_len, 's3_url': url}
        return jsonify({'result': "success", 'video_info': vid_info, 'search_info': search_info, 'res_info': result_list})
    
    except:
        vid_info2 = {'title': title, 's3_url': url, 'video_length': duration, 'length': "0"}
        return jsonify({'result': "fail", 'video_info': vid_info2, 'search_info': search_info})


def groupSequence(lst):
    res = [[lst[0]]]
    for i in range(1, len(lst)):
        if lst[i-1]+1 == lst[i]:
            res[-1].append(lst[i])
        else:
            res.append([lst[i]])
    new = [s for s in res if len(s) > 5]
    new2 = [(i[0], i[-1]) for i in new]
    return new2


@app.route('/api/multiplesearch', methods=['GET'])
def multiplesearch():
    video_id = int(request.args.get('id'))
    person = request.args.get('search_img')
    keyword = request.args.get('search_aud')

    videos = views.get_video_info(video_id)
    title, url, duration = videos[0], videos[1], videos[2]
    search_info = {'search_vid': person, 'search_aud': keyword, 'type': "both"}
    
    try:
        video_detected_seconds = image_search(video_id, person)
    
        audio_sentence_list = []
        for s in coll.find({"video_number":video_id}):
            audio_sentence_list.append(s['sentence_list'])

        audio_detected_seconds = []
        for i in range(len(audio_sentence_list[0])):
            if keyword in audio_sentence_list[0][i]['sentence']:
                audio_detected_seconds.append(round(audio_sentence_list[0][i]['start_time']/1000))

        video_and_audio = []
        for i in range(len(video_detected_seconds)):
            for j in range(len(audio_detected_seconds)):
                if video_detected_seconds[i] == audio_detected_seconds[j]:
                    video_and_audio.append(video_detected_seconds[i])

        path_and_time = []
        for s in coll3.find({"video_pk":video_id}):
            image_list = s['image_list']
            for key in image_list:
                path_and_time.append([key['time'], key['path']])
    
        start_and_path = []
        for i in range(len(video_and_audio)):
            for j in range(len(path_and_time)):
                if video_and_audio[i] == path_and_time[j][0]:
                    start_and_path.append([video_and_audio[i], path_and_time[j][-1]])


        result_list = []
        for i in start_and_path:
            dictionary = {'start': i[0], 'thumbnail': i[-1]}
            dictionary_copy = dictionary.copy()
            result_list.append(dictionary_copy)

        vid_info = {'title': title, 'video_length': duration, 's3_url': url}
        return jsonify({'result': "success", 'video_info': vid_info, 'search_info': search_info, 'res_info': result_list})

    except:
        vid_info2 = {'title': title, 's3_url': url, 'video_length': duration}
        return jsonify({'result': "fail", 'video_info': vid_info2, 'search_info': search_info})