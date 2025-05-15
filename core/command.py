from abc import ABC, abstractmethod
from core.task import Task
from core.composite import TaskList

class Command(ABC):
    """
    Abstract base class for a command.
    """
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddTaskCommand(Command):
    """
    Command to add a task.
    """
    def __init__(self, task_list, task):
        self.task_list = task_list
        self.task = task

    def execute(self):
        self.task_list.add(self.task)

    def undo(self):
        self.task_list.remove(self.task)

class CompleteTaskCommand(Command):
    """
    Command to mark a task as completed.
    """
    def __init__(self, task):
        self.task = task
        self.previous_state = None

    def execute(self):
        self.previous_state = self.task.is_completed
        self.task.is_completed = True

    def undo(self):
        self.task.is_completed = self.previous_state

class CommandInvoker:
    """
    Invoker class to manage command execution and undoing.
    """
    def __init__(self):
        self.history = []

    def execute_command(self, command):
        command.execute()
        self.history.append(command)

    def undo_last_command(self):
        if self.history:
            command = self.history.pop()
            command.undo()

if __name__ == "__main__":
    # Example usage
    task_list = TaskList("Daily Tasks")
    task1 = Task("Buy groceries")
    task2 = Task("Call the doctor")

    add_task_command1 = AddTaskCommand(task_list, task1)
    add_task_command2 = AddTaskCommand(task_list, task2)

    invoker = CommandInvoker()
    invoker.execute_command(add_task_command1)
    invoker.execute_command(add_task_command2)

    # Display tasks
    task_list.display()

    # Undo last command (removing the last added task)
    invoker.undo_last_command()
    task_list.display()