from flask import Flask,jsonify
from .models import setup_db, Book
from flask_cors import CORS

def create_app(test_config =None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods','GET,POST,DELETE,OPTIONS,PUT')
        return response

    @app.route('/books')
    def get_books():
        books = Book.query.all()
        formatted_books = [book.format() for book in books]
        return jsonify({
            'success':True,
            'books':formatted_books
        })

    return app
