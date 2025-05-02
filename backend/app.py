from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, close_db, get_db
# --- REPLACE ALL THESE IMPORTS ---
from database.models import User, Post
from database.db import init_db, close_db, get_db
from database.auth import login_manager
import os
from datetime import datetime

app = Flask(__name__, 
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
app.secret_key = os.getenv('SECRET_KEY') or 'dev-secret-key-123'

# Initialize database and login manager
init_db(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
app.teardown_appcontext(close_db)

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%b %d, %Y %I:%M %p'):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return value.strftime(format)

@app.route('/')
@login_required
def home():
    posts = Post.get_all()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_by_email(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.create(username, email, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        flash('Email already exists', 'error')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    content = request.form['content']
    is_anonymous = 'anonymous' in request.form
    Post.create(content, None if is_anonymous else current_user.id)
    flash('Post created!', 'success')
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    user_posts = Post.get_by_user(current_user.id)
    return render_template('profile.html', user_posts=user_posts)

if __name__ == '__main__':
    app.run(debug=True)