from abc import ABC, abstractmethod
from core.task import TaskComponent, Task

class TaskList(TaskComponent):
    def __init__(self, name):
        self.name = name
        self.components = []

    def add(self, component):
        self.components.append(component)

    def remove(self, component):
        self.components.remove(component)

    def display(self, indent=0):
        print("  " * indent + f"- {self.name}:")
        for component in self.components:
            component.display(indent + 1)

if __name__ == "__main__":
    # Ejemplo de uso del Composite
    task1 = Task("Escribir un correo")
    task2 = Task("Enviar el correo")
    email_tasks = TaskList("Tareas de Correo")
    email_tasks.add(task1)
    email_tasks.add(task2)

    personal_tasks = TaskList("Tareas Personales")
    personal_tasks.add(Task("Hacer ejercicio"))
    personal_tasks.add(email_tasks)
    personal_tasks.display()