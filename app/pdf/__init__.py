
from flask import Blueprint

pdfbp = Blueprint('pdf', __name__, url_prefix='/pdf')

from . import views