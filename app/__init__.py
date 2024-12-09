# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# import sys
# import os
# from config import Config
# import app.models  # Ensure models are imported before db.create_all()

# # Initialize Flask app
# app = Flask(__name__)
# app.config.from_object(Config)  # Use the configuration from config.py

# # Initialize SQLAlchemy
# db = SQLAlchemy(app)

# # Initialize Flask-Login
# login_manager = LoginManager(app)
# login_manager.login_view = 'routes.login'  # Set the login view

# # User loader for Flask-Login
# @login_manager.user_loader
# def load_user(user_id):
#     from app.models import User
#     return User.query.get(int(user_id))

# # Create tables and insert default roles if needed
# with app.app_context():
#     try:
#         print("Creating all tables...")
#         db.create_all()  # Create all tables defined in models
        
#         # Manually check and insert default roles if they don't exist
#         from app.models import Role

#         if not Role.query.first():
#             print("Adding default roles...")
#             db.session.add(Role(name='manager', description='Warehouse Manager'))
#             db.session.add(Role(name='operator', description='Warehouse Operator'))
#             db.session.commit()
#             print("Default roles added.")
#         else:
#             print("Roles already exist.")
    
#     except Exception as e:
#         print(f"Error during table creation or role addition: {str(e)}")
#         sys.exit(1)

# # Import routes and register the blueprint
# from app.routes import routes  # Import routes after app context is set

# try:
#     app.register_blueprint(routes)  # Register the blueprint for the app
#     print("Blueprint registered successfully.")
# except Exception as e:
#     print(f"Error registering blueprint: {e}")
#     sys.exit(1)



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sys
import os
from config import Config
import app.models

# Set up the Flask application
app = Flask(__name__)
app.config.from_object(Config)  # Load app configuration from the Config class

# Initialize the database
db = SQLAlchemy(app)

# Set up Flask-Login for managing user sessions
login_manager = LoginManager(app)
login_manager.login_view = 'routes.login'  # Redirect users to this route if they aren't logged in

# Define how Flask-Login will load a user by their ID
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))  # Fetch the user by ID from the database

# Create database tables and ensure default roles are present
with app.app_context():
    try:
        print("Creating database tables...")
        db.create_all()  # Create tables for all models

        # Add default roles if they are missing
        from app.models import Role
        if not Role.query.first():  # Check if the roles table is empty
            print("Adding default roles...")
            db.session.add(Role(name='manager', description='Warehouse Manager'))
            db.session.add(Role(name='operator', description='Warehouse Operator'))
            db.session.commit()  # Save changes to the database
            print("Default roles added.")
        else:
            print("Default roles already exist.")

    except Exception as e:
        print(f"Error setting up the database: {e}")
        sys.exit(1)  # Stop execution if setup fails

# Import and register the application's routes
from app.routes import routes

try:
    app.register_blueprint(routes)  # Attach the routes blueprint to the app
    print("Routes registered successfully.")
except Exception as e:
    print(f"Error registering routes: {e}")
    sys.exit(1)
