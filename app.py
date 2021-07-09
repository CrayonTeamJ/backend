from flask import Flask, render_template
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.sql.elements import Null
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from forms import LoginForm, RegisterForm

migrate = Migrate()

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] ='Thisissupportedtobesecret!'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://dbmasteruser:password@ls-d8e66d0492f2c70ce3ecd3e603cf642a8c8a8351.cqobb3tz8sun.ap-northeast-2.rds.amazonaws.com/USERinfo'


class user_info(db.Model):
    __tablename__='user_info'
    user_sn = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(150), unique=True, nullable=False)
    user_pw = db.Column(db.String(200), nullable=False)
    user_nick = db.Column(db.String(120), unique=True, nullable=False)
    user_prof = db.Column(db.Text, nullable=True)

    def __init__(self, user_id, user_pw, user_nick, user_prof):
        self.user_id=user_id
        self.user_pw=user_pw
        self.user_nick=user_nick
        self.user_prof=user_prof


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = user_info(user_id=form.userID.data, user_pw=form.password.data, user_nick=form.nickname.data, user_prof='asdfadsf')
        db.session.add(new_user)
        
        db.session.commit()

        return '<h1>New user has been created</h1>'

        

    return render_template('signup.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)