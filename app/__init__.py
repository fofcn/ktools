
import logging
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
    # 创建文件处理器（FileHandler）并设置日志格式
    file_handler = logging.FileHandler('app.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 控制台处理器：将日志输出到控制台
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)


    # 将文件处理器（FileHandler）添加到 Flask 的 logger
    app.logger.addHandler(file_handler) 
    app.logger.addHandler(stream_handler)

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


    return app
