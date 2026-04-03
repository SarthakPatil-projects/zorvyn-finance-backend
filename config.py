import os

class Config:
    SECRET_KEY = "zorvyn-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///finance.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "zorvyn-jwt-secret"