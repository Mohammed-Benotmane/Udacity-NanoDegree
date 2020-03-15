import os
import unittest
import json

from flaskr import create_app
from models import setup_db, Book

class BookTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "fyyur"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','','localhost:5432',self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book = {
            'title':'Anansi Boys',
            'author':'Zakaria',
            'rating': 5
        }

    def tearDown(self):
        pass

    def test_get_pagination_books(self):
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_Books'])
        
if __name__ == "__main__":
    unittest.main()


