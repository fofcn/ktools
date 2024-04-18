
class TaskNotFoundError(Exception):
    """Exception raised when a Task is not found."""

    def __init__(self, task_id, message="Task not found"):
        self.task_id = task_id
        self.message = f"{message}: {task_id}"
        super().__init__(self.message)

class TaskCannotBeCancelledError(Exception):
    """Exception raised when a Task is not found."""

    def __init__(self, task_id, message="Task cannot be cancelled"):
        self.task_id = task_id
        self.message = f"{message}: {task_id}"
        super().__init__(self.message)