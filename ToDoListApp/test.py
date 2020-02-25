from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres@localhost:5432/udacity'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    vehicles = db.relationship('Vehicles',backref='driver',lazy=True)
    def __repr__(self):
        return f'<Driver ID: {self.id} , {self.name} >'

class Vehicles(db.Model):
    __tablename__='vehicules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'),nullable=False)
    def __repr__(self):
        return f'<Vehicles ID: {self.id} , {self.name} , driver: {Driver.query.get(self.driver_id)} >'

db.create_all()

if __name__ =='__main__':
    app.run(debug=True)