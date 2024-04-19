
import atexit
import logging
import signal
import sys
import time
from flask import Blueprint, Flask

from . import config

def create_app(test_config=None):
    app = Flask(__name__)
    app.app_context().push()
    from . import app_holder
    app_holder.add_app(app=app)
    app.config.from_object(config.FlaskConfig)
    app.logger.setLevel(logging.INFO)

    from .log import file_handler, stream_handler

    # 将文件处理器（FileHandler）添加到 Flask 的 logger
    app.logger.addHandler(file_handler) 
    app.logger.addHandler(stream_handler)
    app_holder.add_logger(app.logger)

    from . import error
    app.register_blueprint(error.errbp)

    from . import index
    app.register_blueprint(index.indexbp)

    from .text import csv
    app.register_blueprint(csv.csvbp)

    from . import task
    app.register_blueprint(task.tpbp)

    from . import tp

    from . import pdf
    pdf.init_app(app=app)
    app.register_blueprint(pdf.pdfbp)


    @app.teardown_appcontext
    def teardown_appcontext(error=None):
        print('Tearing down appcontext...')
        tp.executor.shutdown()
        task.w.unregister()

    @atexit.register
    def atexit_callback():
        teardown_appcontext()
    
    def signal_handler(sig, frame):
        teardown_appcontext()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    return app

