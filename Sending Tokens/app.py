from flask import Flask,request,abort

app = Flask(__name__)

def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)
    test = request.headers['Authorization']
    token = test.split(' ')

    if len(token) != 2:
        abort(401)
    elif token[0].lower() != 'bearer':
        abort(401)

    
    return token[1]

@app.route('/headers')
def headers():
    jwt = get_token_auth_header()
    print(jwt)
    return 'nothing'