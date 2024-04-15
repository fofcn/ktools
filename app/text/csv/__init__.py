
from flask import Blueprint


csvbp = Blueprint('csvbp', __name__, url_prefix='/csv')

from . import views