from flask import Flask,jsonify, request
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

    @app.route('/books', methods=['GET','POST'])
    def get_books():
        page= request.args.get('page',1,type=int)
        start= (page-1)*10
        end= start+10
        books = Book.query.all()
        formatted_books = [book.format() for book in books]
        return jsonify({
            'success':True,
            'books':formatted_books[start:end],
            'total_Books': len(formatted_books)
        })

    return app
