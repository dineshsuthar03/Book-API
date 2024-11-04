from flask import Flask
from flask_restful import Api
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/swagger')
def swagger_ui():
    return swagger(app)

# Define your Swagger documentation here if needed
