import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

class DevelopmentConfig(Config):
    DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')
    DEBUG = True

class ProductionConfig(Config):
    DATABASE_URI = os.getenv('PROD_DATABASE_URI', 'sqlite:///prod.db')
    DEBUG = False

class TestingConfig(Config):
    DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test.db')
    TESTING = True
