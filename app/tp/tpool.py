
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, TimeoutError,CancelledError
import multiprocessing
import time
import traceback
import uuid
from .exception import TaskNotFoundError, TaskCannotBeCancelledError

class TaskStatus:
    PENDING = 0
    RUNNING = 1
    COMPLETED = 2
    FAILED = 3
    CANCELLED = 4

class Task(ABC):

    def __init__(self) -> None:
        self.__id = uuid.uuid4()
        self.__status = TaskStatus.PENDING
        self.__kwargs = {}

    def internal_run(self):
        self.status = TaskStatus.RUNNING
        try:
            result = self.run()
            self.status = TaskStatus.COMPLETED
            return result
        except Exception as e:
            traceback.print_exc()
            self.exception = e
            self.status = TaskStatus.FAILED
    def get_id(self):
        return self.__id

    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status
    
    def set_args(self, **kwargs):
        self.__args = kwargs
   
    @abstractmethod
    def run(self):
        pass

class TaskFuture:
    def __init__(self, future, task) -> None:
        self.__future = future
        self.__task = task
        self.__result = None
        self.__exception = None
        self.__cancelled = False

    def get(self, timeout=None):
        if self.__future.done():
            return self.__future.result()
        elif self.__future.cancelled():
            self.__task.set_status(TaskStatus.CANCELLED)
        try:
            self.__result = self.__future.result(timeout)
            if self.__result is not None:
                return self.__result
            else:
                return None
        except TimeoutError:
            return None
        except CancelledError:
            self.__task.set_status(TaskStatus.CANCELLED)
            return None

    def set_result(self, result):
        self.__result = result

    def cancel(self):
        if self.__future.cancelled():
            self.__cancelled = True
        iscancelled = self.__future.cancel()
        if not iscancelled:
            self.__task.set_status(TaskStatus.CANCELLED)
            raise TaskCannotBeCancelledError()
        self.__task.set_status(TaskStatus.CANCELLED)

    def get_status(self):
        return self.__task.get_status()
    
    def get_result(self):
        return self.__result

    def get_exception(self):
        return self.__exception
    
    def cancelled(self):
        return self.__cancelled

class PdfSplitterTask(Task):
    def __init__(self, pdf_path, page_num, output_path) -> None:
        super().__init__()
        self.pdf_path = pdf_path
        self.page_num = page_num
        self.output_path = output_path

    def run(self):
        print('executed pdf splitter')
        time.sleep(5)
        print('executed pdf splitter completed')
        return "split pdf to pieces"

class TaskExecutor:
    
    def __init__(self, pnum) -> None:
        self.taskpool = ThreadPoolExecutor(max_workers=pnum)

    def __execute_task(self, task):
        task_result = task.internal_run()
        return task_result

    def submit_task(self, task):
        future = self.taskpool.submit(self.__execute_task, task)
        return TaskFuture(future, task)

    def close(self):
        with self.lock:
            self.tasktable.clear()
        
        self.taskpool.shutdown(wait=True)


class TaskFutureTable:

    def __init__(self) -> None:
        self.table = {}
        self.lock = multiprocessing.Lock()

    def add(self, id, future):
        with self.lock:
            self.table[id] = future

    def remove(self, id):
        with self.lock:
            del self.table[id]
    
    def get(self, id):
        with self.lock:
            return self.table[id]


class ExecutorController:

    def __init__(self, workernum) -> None:
        self.__executor = TaskExecutor(workernum)
        self.__futuretable = TaskFutureTable()
        self.__kwargs = {}

    def init(self, **kwargs):
        self.__kwargs = kwargs

    def before_exec(self, **kwargs):
        pass

    def submit_task(self, task):
        print("submit task")
        self.before_exec(**self.__kwargs)
        future = self.__executor.submit_task(task)
        self.__futuretable.add(task.get_id(), future)
    
    def cancel_task(self, task_id):
        future = self.__futuretable.get(task_id)
        if future is None:
            raise TaskNotFoundError()
        
        try:
            future.cancel()
        except Exception:
            pass
        finally:
            self.__futuretable.remove(task_id)

    def get_result(self, task_id, timeout=None):
        future = self.__futuretable.get(task_id)
        if future is None:
            raise TaskNotFoundError()
        result = future.get(timeout)
        if result is None:
            return None, future.get_status()
        
        return result, future.get_status()
