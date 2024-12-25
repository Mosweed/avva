import os 
from dotenv import load_dotenv 
 
load_dotenv() 
 
class Config:
    
    # General settings 
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key') 
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't') 
    PROJECT_NAME = os.getenv("PROJECT_NAME") 
    
    # MySQL settings
    MYSQL_HOST = os.getenv("MYSQL_HOST") 
    MYSQL_USER = os.getenv("MYSQL_USER")  # 'mydatabase' 
    MYSQL_DB = os.getenv("MYSQL_DB")  # 'myusername' 
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")  # 'mypassword' 
    MYSQL_PORT = os.getenv("MYSQL_PORT") 
    
    # Mail settings
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER") 
    
class DevelopmentConfig(Config): 
    FLASK_ENV = 'development' 
    DEBUG = True 
 
class ProductionConfig(Config): 
    FLASK_ENV = 'production' 
    DEBUG = False 
 
class TestingConfig(Config): 
    TESTING = True 
    DEBUG = True 
 
config = { 
    'development': DevelopmentConfig, 
    'production': ProductionConfig, 
    'testing': TestingConfig, 
} 
