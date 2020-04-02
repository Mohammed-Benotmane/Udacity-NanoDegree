from flask import Flask,request

app = Flask(__name__)

@app.route('/headers')
def headers():
    test = request.headers['Authorization']
    token = test.split(' ')[1]
    print(token)
    return 'nothing'