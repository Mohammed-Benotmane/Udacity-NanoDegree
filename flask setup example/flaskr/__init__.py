from flask import Flask,jsonify
from models import setup_db, Plant
from flask_cors import CORS

def create_app(test_config =None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def hello():
        return jsonify({
            'message':'bonjour comon talé vou'
        })
    
    @app.route('/smiley/<kima>')
    def smiley(kima):
        return 'XD'+ kima

    return app
