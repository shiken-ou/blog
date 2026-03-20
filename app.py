from flask import Flask, render_template, url_for, flash, request
from flask_login import LoginManager, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from sqlalchemy import select
from config import DevelopmentConfig
from database import engine, SessionLocal
from models import Base, User, Post
from forms import forms_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'forms.login'
app.register_blueprint(forms_bp)

Base.metadata.create_all(engine)


@login_manager.user_loader
def load_user(id: str)-> User:
    with SessionLocal() as session:
        stmt = select(User).where(User.id == id)
        user = session.scalars(stmt).one()
    return user

def load_post(id: int)-> Post:
    with SessionLocal() as session:
        stmt = select(Post).where(Post.id == id)
        post = session.scalars(stmt).one()
    return post

@app.get('/')
def index():
    with SessionLocal() as session:
        stmt = select(Post).order_by(Post.created_at.desc())
        posts = session.scalars(stmt).all()
    
    return render_template('index.html', posts = posts)


@app.get('/post/<int:id>')
def show_post(id):
    post = load_post(id)
    return render_template('post.html', post= post)


@app.route('post/new')
def create_post():
    pass

@app.post('/post/<int:id>/delete')
@login_required
def delete_post(id):
    post = load_post(id)
    try:
        with SessionLocal() as session:
            session.delete(post)
            session.commit()
    except:
        flash('削除失敗', 'error')
        return url_for('show_post', id= id)
    else:
        flash('削除済み', 'sucess')

    return url_for('index')


class EditForm(FlaskForm):
    title = StringField(
        'タイトル',
        validators= [
            DataRequired('タイトルを入力してください'),
            Length(max= 50, message= 'タイトルは50文字以内にお願いします')
        ]
    )

    content = TextAreaField(
        '文章',
        validators= [
            DataRequired('文章を入力してください'),
            Length(max= 3000, message= '文の文字数は3000文字以内にお願いします')
        ]
    )

    submit = SubmitField('完了')


@app.route('/post/<int:id>/edit', method= ['GET', 'POST'])
@login_required
def edit_post(id):
    post = load_post(id)

    if request.method == 'GET':
        form = EditForm(obj= post)

    if form.validate_on_submit():
        try:
            with SessionLocal() as session:
                post.title = form.title.data
                post.content = form.content.data
                session.commit()
        except:
            flash('編集失敗', 'error')
            return url_for('show_post', id= id)
        else:
            flash('削除済み', 'sucess')
        
    return render_template('edit.html', post= post)