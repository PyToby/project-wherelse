from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import User, Comparison, UserHistory, db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('view.home'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@auth.route('/signup', methods=["POST"])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    user = User.query.filter_by(email=email).first()
    if not user:
        if password == confirm_password:
            new_user = User(email=email)
            new_user.set_password(password)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect('/')
            except Exception as e:
                db.session.rollback()
                print(f"Signup error: {e}")  # shows in Render logs
                return render_template('login.html', error=f'Error: {str(e)}')
        else:
            return render_template('login.html', error='Passwords do not match')
    else:
        return render_template('login.html', error='Email already registered')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')