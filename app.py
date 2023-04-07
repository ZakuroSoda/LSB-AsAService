from flask import Flask, render_template, request, redirect, url_for, send_file
from uuid import uuid4
from stegolib import Encode, Decode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    image = request.files['file']
    secret = request.form['secret']

    if image.mimetype != 'image/png':
        return redirect(url_for('index'))
    
    filename = 'uploads/' + uuid4().hex + '.png'
    image.save(filename)

    encoded_filename = Encode(filename, 'uploads/' + uuid4().hex + '.png', secret)
    print(encoded_filename)
    if encoded_filename is None:
        return redirect(url_for('index'))
    
    message = Decode(encoded_filename)
    print(message)

    return redirect(f'/download/{encoded_filename}')

@app.route('/download/uploads/<filename>')
def download(filename):
    return send_file(f"uploads/{filename}", as_attachment=True)

@app.route('/decode', methods=['POST'])
def decode():
    image = request.files['file']

    if image.mimetype != 'image/png':
        return redirect(url_for('index'))
    
    filename = 'uploads/' + uuid4().hex + '.png'
    image.save(filename)

    message = Decode(filename)
    if message is None:
        return render_template('decoded.html', message="Your image doesn't contain any secret message.")
    
    return render_template('decoded.html', message=f"Message: {message}")

app.run(debug=True, host="0.0.0.0", port=80)