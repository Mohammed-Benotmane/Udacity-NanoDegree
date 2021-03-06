import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question':'where is situated Algeria?',
            'answer':'North Africa',
            'difficulty':3,
            'category': 3
        }

        self.new_question_fake = {
            'question':'where is situated Algeria?',
            'answer':'North Africa',
            'difficulty':3,
            'category': "science"
        }
        self.category = Category.query.filter(Category.id == 3).one_or_none().format()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(data['categories'])

    def test_delete_questions(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 4).one_or_none()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],4)
        self.assertTrue(data['questions'])
        self.assertEqual(question,None)

    def test_create_question(self):
        res = self.client().post('/questions',json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)


    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/categories/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_post_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'e'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_422_create_question(self):
        res = self.client().post('/questions',json=self.new_question_fake)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['category'])

    def test_play_quiz(self):
        res = self.client().post('/quizzes',json={
        "previous_questions":[9],
        "quiz_category":{
    	"id":5,
    	"type":"Sports"
    }})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['previous_questions'])
        self.assertTrue(data['question'])






        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()