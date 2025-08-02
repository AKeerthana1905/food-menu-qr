from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Password validation regex
PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

# ------------------- ROUTES -------------------

@app.route('/')
def home():
    return render_template('login.html')  # Login is now the homepage

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate password
        if not re.match(PASSWORD_PATTERN, password):
            flash("Password must have at least 8 characters, 1 uppercase letter, 1 number, and 1 special character.")
            return redirect(url_for('login'))

        # Successful login
        session['user'] = username
        return redirect(url_for('upload_page'))

    return render_template('login.html')

@app.route('/upload_page')
def upload_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user' not in session:
        return {'success': False, 'message': 'Not logged in'}

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

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ------------------- MAIN -------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
