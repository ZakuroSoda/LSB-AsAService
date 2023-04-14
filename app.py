from flask import Flask, render_template, request, redirect, send_from_directory, url_for, send_file
from uuid import uuid4
from stegolib import Encode, Decode
import os

app = Flask(__name__)

upload_dir = os.path.join(app.instance_path, 'uploads')
download_dir = os.path.join(app.instance_path, 'downloads')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encode', methods = ['POST'])
def encode():
    image = request.files['file']
    secret = request.form['secret']

    if image.mimetype != 'image/png':
        return 'So sorry, we only support PNG images at this period of time.', {"Refresh": f"1; {url_for('index')}"}

    filedir = os.path.join(upload_dir, f'{uuid4().hex}.png')
    image.save(filedir)
    encoded_fileuuid = uuid4().hex
    encoded_filedir = Encode(filedir, os.path.join(download_dir, f'{encoded_fileuuid}.png'), secret)
    if encoded_filedir == None:
        return 'So sorry, an error occured.', {"Refresh": f"1; {url_for('index')}"}
    return redirect(url_for('download', fileuuid=encoded_fileuuid))

@app.route('/download/<fileuuid>')
def download(fileuuid):
    if not f'{fileuuid}.png' in os.listdir(download_dir):
        return 'So sorry, an error occured.', {"Refresh": f"1; {url_for('index')}"}
    return send_from_directory(download_dir, f'{fileuuid}.png')

@app.route('/decode', methods=['POST'])
def decode():
    image = request.files['file']
    if image.mimetype != 'image/png':
        return 'So sorry, we only support PNG images at this period of time.', {"Refresh": f"1; {url_for('index')}"}
    
    filedir = os.path.join(upload_dir, f'{uuid4().hex}.png')
    image.save(filedir)
    message = Decode(filedir)
    if message == None:
        return render_template('decoded.html', message="Your image doesn't contain any secret message.")
    return render_template('decoded.html', message=f"Message: {message}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
