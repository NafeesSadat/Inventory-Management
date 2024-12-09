import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '51b09c8745386c2b01ca6f7846faad16'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:*Sadat123@localhost:5432/warehouse_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 200  # Increase connection pool size
    SQLALCHEMY_MAX_OVERFLOW = 300  # Increase max overflow
    SQLALCHEMY_POOL_TIMEOUT = 100  # Set pool timeout
    SQLALCHEMY_ECHO = True  # query logging

