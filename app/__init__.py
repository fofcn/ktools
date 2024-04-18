
import logging
import time
from flask import Blueprint, Flask
from . import config

def create_app(test_config=None):
    app = Flask(__name__)
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

    from . import pdf
    app.register_blueprint(pdf.pdfbp)

    from . import task
    app.register_blueprint(task.tpbp)

    tpool = task.ExecutorController(config.FlaskConfig.TASK_POOL_NUM)
    t = task.PdfSplitterTask('', 20, './tmp/')
    tpool.submit_task(t)
    
    for i in range(10):
        # print(f'executed {i}th time')
        result, status = tpool.get_result(t.get_id(), 2)
        if task.TaskStatus.CANCELLED == status or task.TaskStatus.FAILED == status:
            print(f"Task is cancelled or failed: {status}\n")
            break
        elif task.TaskStatus.RUNNING == status:
            print(f'tpool task status {status}, result: {result}')
        elif task.TaskStatus.COMPLETED == status:
            print(f'tpool task completed')
        time.sleep(1)

    return app