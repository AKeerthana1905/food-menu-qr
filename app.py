from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('Menu.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'menu' not in request.files:
        return redirect(request.url)

    file = request.files['menu']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return {'success': True, 'filename': filename}

    return {'success': False}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)