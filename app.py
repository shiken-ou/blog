from flask import Flask, render_template, url_for, flash, request
from flask_login import LoginManager, current_user, login_required
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session
from config import DevelopmentConfig
from models import Base, User, Post
from forms import forms_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'forms.login'
app.register_blueprint(forms_bp)

engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(engine)


@login_manager.user_loader
def load_user(id: str)-> User:
    with Session(engine) as session:
        stmt = select(User).where(User.id == id)
        user = session.scalars(stmt).one()
    return user

def load_post(id: int)-> Post:
    with Session(engine) as session:
        stmt = select(Post).where(Post.id == id)
        post = session.scalars(stmt).one()
    return post

@app.get('/')
def index():
    with Session(engine) as session:
        stmt = select(Post).order_by(Post.created_at.desc())
        posts = session.scalars(stmt).all()
    
    return render_template('index.html', posts = posts)


@app.get('/post/<int:id>')
def show_post(id):
    post = load_post(id)
    return render_template('post.html', post= post)


@app.post('/post/<int:id>/delete')
@login_required
def delete_post(id):
    post = load_post(id)
    try:
        with Session(engine) as session:
            session.delete(post)
            session.commit()
    except:
        flash('削除失敗', 'error')
        return url_for('show_post', id= id)
    else:
        flash('削除済み', 'sucess')

    return url_for('index')

@app.route('/post/<int:id>/edit', method= ['GET', 'POST'])
@login_required
def edit_post(id):
    post = load_post(id)
    if request.method == 'POST':
        try:
            with Session(engine) as session:
                post.title = request.form.get('title')
                post.content = request.form.get('content')
                session.commit()
        except:
            flash('編集失敗', 'error')
            return url_for('show_post', id= id)
        else:
            flash('削除済み', 'sucess')
        
    return render_template('edit.html', post= post)