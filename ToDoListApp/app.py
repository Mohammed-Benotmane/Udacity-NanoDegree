from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',data=[{
        'description': 'todo1'
    },
    {
        'description': 'todo2'
    },
    {
        'description': 'todo3'
    },
    ])
    