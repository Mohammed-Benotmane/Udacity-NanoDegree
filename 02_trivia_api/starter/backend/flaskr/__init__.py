import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
  CORS(app, resources={r"/api/*": {"origins": "*"}})
 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods','GET,POST,DELETE,OPTIONS,PUT')
      return response
 
  @app.route('/categories',methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    return jsonify({
      'success':True,
      'categories':formatted_categories,
      'total_categories':len(categories)
    })

 
  @app.route('/questions',methods=['GET'])
  def get_questions():
    page= request.args.get('page',1,type=int)
    start= (page-1)*QUESTIONS_PER_PAGE
    end= start+QUESTIONS_PER_PAGE
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.all()
    formatted_categories=  [category.format() for category in categories]
    return jsonify({
      'success':True,
      'questions':formatted_questions[start:end],
      'total_questions':len(questions),
      'categories': formatted_categories
    })


 
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    if question is None:
      abort(404)
    question.delete()
    questions = Question.query.all()
    return jsonify({
      'success':True,
      'deleted':question_id,
      'questions':[question.format() for question in questions]
    })


 
  @app.route('/questions',methods=['POST'])
  def create_question():
    body = request.get_json()
    if(body.get("searchTerm")):
      search_term = body.get("searchTerm")
      temp = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      questions = [t.format() for t in temp]
      if(len(temp)==0):
        abort(404)
      return jsonify({
        'success':True,
        'questions': questions,
        'total_questions': len(temp),
        'current_category':1
      })
    else:
      new_question = body.get("question",None)
      new_category = body.get("category",None)
      new_answer = body.get("answer",None)
      new_difficulty=body.get("difficulty",None)
      try:
        question = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
        question.insert()
      except:
        abort(422)
      questions=Question.query.all()
      formatted_questions= [qst.format() for qst in questions]
      return jsonify({
        'success':True,
        'questions':formatted_questions,
        'total_questions':len(questions)
      })
    
  
  @app.route('/categories/<int:category_id>/questions',methods=['GET'])
  def get_questions_by_category(category_id):
    category= Category.query.filter(Category.id== category_id).one_or_none()
    if(category is None):
      abort(404)
    questions = Question.query.filter(Question.category == category.id).all()
    formatted_questions = [question.format() for question in questions]
    return jsonify({
      'success':True,
      'category':category.id,
      'questions':formatted_questions,
      'total_questions':len(questions)
    })

  @app.route('/quizzes',methods=['POST'])
  def play_quiz():
    body= request.get_json()
    previous_question = body.get('previous_questions')
    category = body.get('quiz_category')
    if ((category is None) or (previous_question is None)):
      abort(404)
    
    
    if(category["type"] == "click"):
      questions = Question.query.all()
    else:
      category_id =int(category["id"]) + 1
      questions = Question.query.filter(Question.category==category_id).all()
    
    random_question = random.choice(questions)
    def is_used(question):
      used = False
      if question.id in previous_question:
        used =True
      return used
    if(len(previous_question)== len(questions)):
        return jsonify({
          'success':True,
          'question':None,
          'previous_questions':previous_question
        })
    while(is_used(random_question)):
      random_question = random.choice(questions)
      
    return jsonify({
      'success':True,
      'question':random_question.format(),
      'previous_questions':previous_question
    })

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "500 Internal Server Error” "
      }), 500

  @app.route('/')
  def hello():
    return jsonify({
      'success':True
    })
  return app

    