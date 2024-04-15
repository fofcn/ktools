
from flask import current_app
from . import errbp
from .exceptions import custom

@errbp.app_errorhandler(404)
def not_found(error):
    return '<h1>404</h1>', 404

@errbp.app_errorhandler(500)
def internal_server_error(error):
    return '<h1>500</h1>', 500

@errbp.app_errorhandler(Exception)
def internal_server_error(e):
    current_app.logger.exception('custom excepiton')
    return str(e), 400

@errbp.errorhandler(custom.CustomError)
def handle_custom_error(error):
    return error.message, error.code
