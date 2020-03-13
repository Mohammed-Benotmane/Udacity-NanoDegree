from flask import Flask,jsonify, request, abort
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


    @app.route('/books/<int:book_id>',methods=['PATCH'])
    def update_book(book_id):
        body =request.get_json()
        try:
            book = Book.query.filter(Book.id== book_id).one_or_none()
        
            if book is None:
                abort(404)
            
            if 'rating' in body:
                book.rating = int (body.get('rating'))

            book.update()
            return jsonify({
                'success':True,
                'id':book.id
            })
        except:
            abort(400)

    @app.route('/books', methods=['GET'])
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
    
    @app.route('/books/<int:book_id>')
    def get_specific_book(book_id):
        book = Book.query.filter(Book.id== book_id).one_or_none()
        if book is None:
            abort(404)
        else:
            return jsonify({
                'success':True,
                'book': book.format()
            })

    @app.route('/books/<int:book_id>',methods=['DELETE'])
    def delete_book(book_id):
        book = Book.query.filter(Book.id== book_id).one_or_none()
        books = Book.query.all()
        if book is None:
            abort(404)
        book.delete()
        return jsonify({
            'success':True,
            'deleted':book_id
        })

    return app
