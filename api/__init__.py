from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_graphql import GraphQLView
from .graphql_schema import schema

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    
    # Register blueprints and create database tables
    with app.app_context():
        from .auth import auth_bp
        from .hash_cracker import hash_cracker_bp
        from .models import User, HashResult
        db.create_all()
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(hash_cracker_bp)
        app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
        
    return app

