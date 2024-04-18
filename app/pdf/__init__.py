
from flask import Blueprint

bpapp = None

def init_app(app):
    global bpapp
    bpapp = app

pdfbp = Blueprint('pdf', __name__, url_prefix='/pdf')

from . import views
