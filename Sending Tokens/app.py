from flask import Flask,request

app = Flask(__name__)

@app.route('/headers')
def headers():
    test = request.headers['Authorization']
    print(test)
    return 'nothing'