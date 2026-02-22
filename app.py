import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

# Import from local modules
from config import Config
from models import db, User, Location

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Setup Logging
logging.basicConfig(filename='activity.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        logging.info(f"New user registered: {email}")
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            logging.info(f"User logged in: {email}")
            return redirect(url_for('dashboard'))
        
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logging.info(f"User logged out: {current_user.email}")
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    history = Location.query.filter_by(user_id=current_user.id).order_by(Location.timestamp.desc()).limit(20).all()
    last_loc = history[0] if history else None
    return render_template('dashboard.html', history=history, last_loc=last_loc)

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Access Denied: Admins Only', 'danger')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    user_data = []
    for u in users:
        latest = Location.query.filter_by(user_id=u.id).order_by(Location.timestamp.desc()).first()
        user_data.append({
            'user_id': u.id,
            'email': u.email,
            'is_admin': u.is_admin,
            'lat': latest.latitude if latest else None,
            'lng': latest.longitude if latest else None,
            'last_seen': latest.timestamp.strftime('%Y-%m-%d %H:%M') if latest else 'Never'
        })
        
    return render_template('admin.html', user_data=user_data)

@app.route('/api/update_location', methods=['POST'])
@login_required
def update_location():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    
    if lat and lng:
        new_loc = Location(
            user_id=current_user.id,
            latitude=float(lat),
            longitude=float(lng)
        )
        db.session.add(new_loc)
        db.session.commit()
        return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@tracker.com').first():
            admin = User(
                email='admin@tracker.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)