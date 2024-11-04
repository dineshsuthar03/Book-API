from flask_restful import Resource
from flask import request, jsonify
from models import Book, User, db
from werkzeug.security import check_password_hash, generate_password_hash
from html import escape

tokens = {}

def verify_token(request):
    # Extract the token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None  # No valid Authorization header provided
    token = auth_header.split(' ')[1]  # Get the token part after 'Bearer '
    return token if token in tokens.values() else None

class BookResource(Resource):
    def get(self):
        token = verify_token(request)
        if not token:
            return {'message': 'Unauthorized access.'}, 401

        books = Book.query.all()
        return [
            {'id': book.id, 'title': escape(book.title), 'author': escape(book.author),
             'year': book.year, 'genre': escape(book.genre)}
            for book in books
        ], 200

    def post(self):
        token = verify_token(request)
        if not token:
            return {'message': 'Unauthorized access.'}, 401

        data = request.get_json()
        new_book = Book(
            title=escape(data['title']),
            author=escape(data['author']),
            year=data['year'],
            genre=escape(data['genre'])
        )

        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added successfully.'}, 201

class UserResource(Resource):
    def post(self):
        data = request.get_json()
        username = escape(data['username'])
        password = escape(data['password'])
        hashed_password = generate_password_hash(password)

        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully.'}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = escape(data['username'])
        password = escape(data['password'])

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            token = f"token-{user.id}"
            tokens[username] = token
            return {'token': token}, 200

        return {'message': 'Invalid username or password'}, 401

def initialize_resources(api):
    api.add_resource(BookResource, '/api/books')
    api.add_resource(UserResource, '/api/register')
    api.add_resource(LoginResource, '/api/login')