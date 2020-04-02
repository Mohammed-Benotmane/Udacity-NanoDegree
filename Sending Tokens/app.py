from flask import Flask,request,abort

app = Flask(__name__)

@app.route('/headers')
def headers():
    if 'Authorization' not in request.headers:
        abort(401)
    test = request.headers['Authorization']
    token = test.split(' ')[1]
    print(token)
    return 'nothing'