import os
import uuid

import pandas as pd
from flask import Flask, render_template, request, send_from_directory, redirect, url_for

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/convert_csv', methods=['POST'])
def convert_csv():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    try:
        # Explicitly specify the engine based on the file extension
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(file, engine='openpyxl')
        elif file.filename.endswith('.xls'):
            df = pd.read_excel(file, engine='xlrd')
        else:
            return "Unsupported file format. Please upload a .xlsx or .xls file.", 400
    except Exception as e:
        return f"Error reading the file: {str(e)}", 400

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads', filename), index=False)

    return render_template('download.html', filename=filename)


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('downloads', filename, download_name='result.csv')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)