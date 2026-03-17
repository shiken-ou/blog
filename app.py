from flask import Flask
from config import DevelopmentConfig
from forms import forms_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(forms_bp)

@app.get('/')
def index():
    pass