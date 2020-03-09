from flask import Flask,jsonify

def create_app(test_config =None):
    app = Flask(__name__)
    @app.route('/')
    def hello():
        return jsonify({
            'message':'bonjour comon talé vou'
        })
    
    @app.route('/smiley/<kima>')
    def smiley(kima):
        return 'XD'+ kima

    return app
