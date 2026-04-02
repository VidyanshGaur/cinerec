from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if email exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))

        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(name=name, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        flash('Account created! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('movies.dashboard'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))