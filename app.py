from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import insert
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import Email, InputRequired, Length
import config
from forms import LoginForm, RegisterForm


app = Flask(__name__)

db = SQLAlchemy()

migrate = Migrate() 

  
app.config.from_object(config)
db.init_app(app)
migrate.init_app(app, db)

from models import user_info
import views
Bootstrap(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = user_info.query.filter_by(user_id=form.userID.data).first()
        if user:
            if user.user_pw == form.password.data:
                return redirect(url_for('dashboard'))
            
        return '<h1>Invalid username of password</h1>'

    return render_template('login.html', form=form)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        views.user_insert(form.userID.data, form.password.data, form.nickname.data)
        

        return '<h1>New user has been created</h1>'

        

    return render_template('signup.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    manager .run(debug=True)
