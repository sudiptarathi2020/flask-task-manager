from flask import Flask, render_template

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    value = 'Disputant'
    result = 20 + 40
    mylist = [10,20,30,40]
    return render_template('index.html',mylist=mylist)

@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)
