
from flask import Blueprint

tpbp = Blueprint('tp', __name__, url_prefix='/task')
from . import views
from . import worker

w = worker.Worker()
w.register()
