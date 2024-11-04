from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_restful import Api
from config import Config
from resources import initialize_resources
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    # Initialize resources for RESTful API
    api.init_app(app)
    initialize_resources(api)

    # Secret key for session management (add to your Config class in config.py)
    app.secret_key = app.config.get("SECRET_KEY", "default_secret_key")

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password)
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                # Generate a simple token (ideally use JWT or another secure method)
                token = f"token-{user.id}"
                session['token'] = token  # Store token in session for use in frontend
                flash('Login successful!')
                return redirect(url_for('books'))
            flash('Invalid credentials.')
        return render_template('login.html')

    @app.route('/books')
    def books():
        # Check if token is present in the session
        if 'token' not in session:
            flash("Please log in to access the books page.")
            return redirect(url_for('login'))
        return render_template('books.html')

    @app.route('/logout')
    def logout():
        session.pop('token', None)  # Clear token from session on logout
        flash("Logged out successfully.")
        return redirect(url_for('login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
