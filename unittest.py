import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import inspect
from app import models
import os
import sys
from app.routes import routes

# FILE: app/test___init__.py


class TestAppInit(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_warehouse.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        self.db = SQLAlchemy(self.app)
        self.migrate = Migrate(self.app, self.db)
        self.login_manager = LoginManager(self.app)
        self.login_manager.login_view = 'routes.login'
        self.app.app_context().push()

    def tearDown(self):
        self.db.drop_all()
        os.remove('test_warehouse.db')

    def test_table_creation(self):
        with self.app.app_context():
            self.db.create_all()
            inspector = inspect(self.db.engine)
            tables = inspector.get_table_names()
            self.assertIn('user', tables)
            self.assertIn('role', tables)

    def test_role_existence_and_addition(self):
        with self.app.app_context():
            self.db.create_all()
            if not models.Role.query.first():
                self.db.session.add(models.Role(name='manager', description='Warehouse Manager'))
                self.db.session.add(models.Role(name='operator', description='Warehouse Operator'))
                self.db.session.commit()
            roles = models.Role.query.all()
            self.assertEqual(len(roles), 2)
            self.assertEqual(roles[0].name, 'manager')
            self.assertEqual(roles[1].name, 'operator')

    def test_blueprint_registration(self):
        with self.app.app_context():
            try:
                self.app.register_blueprint(routes)
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"Blueprint registration failed: {e}")

if __name__ == '__main__':
    unittest.main()
