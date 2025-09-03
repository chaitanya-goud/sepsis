import os
from dotenv import load_dotenv

load_dotenv()

def _normalized_database_url():
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('postgres://'):
        # SQLAlchemy expects 'postgresql+psycopg2://'
        db_url = db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
    return db_url


class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = _normalized_database_url() or 'sqlite:///sepsis_prediction.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Model paths (PyTorch)
    MODEL_PATH = os.environ.get('MODEL_PATH') or 'model/cnn_lstm_model.pth'
    SCALER_PATH = os.environ.get('SCALER_PATH') or 'model/scaler.pkl'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use environment variables for production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required for production")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 
