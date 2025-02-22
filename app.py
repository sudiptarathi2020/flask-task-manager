from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/hello', methods=['GET','POST'])
def hello():
    response = make_response('Hello World')
    response.status_code = 202
    response.headers['content-type'] = 'application/json'
    return response
@app.route('/add/<int:number1>/<int:number2>')
def add(number1, number2):
    return f'{number1} + {number2} = {number1 + number2}'


@app.route('/handle_url_params')
def handle_url_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
        return f'{greeting}, {name}'
    else:
        return 'Some Parameters are missing'


@app.route('/greet/<name>')
def greet(name):
    return f"Hello {name}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)
