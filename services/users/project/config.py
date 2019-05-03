# services/users/project/config.py
import os  # nuevo


class BaseConfig:
    """Configuracion base"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_secretkey'


class DevelopmentConfig(BaseConfig):
    """Configuracion de Desarrollo"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """Configuracion de Prueba"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Configuracion de produccion"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
