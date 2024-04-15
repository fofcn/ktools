
import os


class FlaskConfig:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/supply_chain"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # JWT
    JWT_SECRET_KEY = '123456'

    # NAS
    NAS_STORE_PATH = os.environ.get('NAS_STORE_PATH')
    