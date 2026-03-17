from flask import Blueprint, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import engine, User
from werkzeug.security import check_password_hash

forms_bp = Blueprint('forms', __name__)

class LoginForm(FlaskForm):
    username = StringField(
        'ユーザー名',
        validators= [DataRequired(message='ユーザー名を入力してください')]
    )

    password = PasswordField(
        'パスワード',
        validators= [DataRequired(message= 'パスワードを入力してください')]
    )

    submit = SubmitField('ログイン')


@forms_bp.route('/login', methods= ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        
        with Session(engine) as session:
            stmt = select(User).where(User.username == username)
            user = session.scalars(stmt).one()
            if user:
                if check_password_hash(user.password_hash, password):
                    flash('ログイン成功', 'success')
                    return url_for('admin')
            flash('無効なユーザー名またはパスワードです', 'fail')
    
    return render_template('login.html', form= form)