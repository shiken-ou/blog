from flask import Blueprint, url_for, render_template, flash, redirect
from flask_wtf import FlaskForm
from flask_login import login_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import select
from werkzeug.security import check_password_hash
from database import SessionLocal
from models import User

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
        password = form.password.data
        
        with SessionLocal() as session:
            stmt = select(User).where(User.username == username)
            user = session.scalars(stmt).first()
            if user:
                if check_password_hash(user.password_hash, password):
                    login_user(user, remember= True)
                    flash('ログイン成功', 'success')
                    return redirect(url_for('index'))
            flash('無効なユーザー名またはパスワードです', 'error')
    
    return render_template('login.html', form= form)