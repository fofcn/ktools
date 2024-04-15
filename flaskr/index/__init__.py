from flask import Blueprint

indexbp = Blueprint('index', __name__)

from . import views