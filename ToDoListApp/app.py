from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres@localhost:5432/udacity'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
migrate = Migrate(app , db)
class ToDoList(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String(), nullable= False)
    completed = db.Column(db.Boolean, nullable= False,default=False)
    def __repr__(self):
        return f'< ToDo ID: {self.id} , description : {self.description} >'

@app.route('/')
def index():
    return render_template('index.html',data=ToDoList.query.order_by('id').all())

@app.route('/todos/create', methods=['POST'])
def create():
    error = False
    try:
     descr = request.get_json()['description']
     db.session.add(ToDoList(description=descr))
     db.session.commit()
     print(descr)
    except:
     error = True
     print(sys.exc_info())
     db.session.rollback()
    finally:
     db.session.close()
     if not error:
      return jsonify({
          'description' : descr
      })

@app.route('/todos/<todo_id>/set_completed', methods=['POST'])
def set_completed(todo_id):
    error = False
    try: 
        temp = request.get_json()['completed']
        todo = ToDoList.query.get(todo_id)
        todo.completed = temp
        db.session.commit()
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
        if not error:
            return redirect(url_for('index'))


@app.route('/todos/<cross_id>/deleted', methods=['DELETE'])
def deleted(cross_id):
    error = False
    try:
        ToDoList.query.filter(ToDoList.id== cross_id).delete()
        db.session.commit()
    except:
        error= True
        print(sys.exc_info())
        db.session.rollback
    finally:
        db.session.close()
        return redirect(url_for('index'))

