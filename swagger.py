from flask import Flask, request
from sqlalchemy.sql.sqltypes import String
from app import app
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields
import views

api = Api(app, version='1.0', title='SEA FLAG API', description='SEA FLAG API입니다') # API 만든다
ns  = api.namespace('api', description='API') # /detect/ 네임스페이스를 만든다

# REST Api에 이용할 데이터 모델을 정의한다
model_signup = api.model('signup_form', {

    'userID': fields.String(required=True, description='아이디', help='아이디는 필수'),
    'password': fields.String(required=True, description='비밀번호', help='비밀번호는 필수'),
    'nickname': fields.String(required=True, description='닉네임', help='닉네임은 필수'),
})

model_login = api.model('login_form', {
    'userID': fields.String(required=True, description='아이디', help='아이디는 필수'),
    'password': fields.String(required=True, description='비밀번호', help='비밀번호는 필수'),
})



@ns.route('/signup') # 네임스페이스 x.x.x.x/detect 하위 / 라우팅
class Mainclass(Resource):
    @ns.doc(responses={ 200: 'OK', 202: 'ID_duplicated Error', 203: 'NK_duplicate Error' })
    @ns.expect(model_signup)
    def post(self):
        
        pass

@ns.route('/login')
class Mainclass(Resource):
    @ns.doc(responses={ 200: 'OK', 203: 'Login Fail'})
    @ns.expect(model_login)
    def post(self):
        #api.payload['Reasult'] = views.user_login(api.payload['userID'], api.payload['password'])
        pass

@ns.route('/refresh')

class Refresh(Resource):
    parser = api.parser()
    parser.add_argument('cookie', location='headers')
    @api.expect(parser)
    @ns.doc(responses={ 200: 'OK', 422: 'No Refresh Token'})
    def get(self):
        pass

@ns.route('/input')
class Input(Resource):
    parser = api.parser()
    parser.add_argument('image_type', type=String, location='form')
    parser.add_argument('file', type=werkzeug.FileStorage, location='files')
    @api.expect(parser)
    def post(self):
        pass
