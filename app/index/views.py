
from .import indexbp

@indexbp.route('/')
def index():
    return 'Hello KTools'