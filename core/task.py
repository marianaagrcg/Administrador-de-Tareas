from abc import ABC, abstractmethod

class TaskComponent(ABC):
    @abstractmethod
    def display(self, indent=0):
        pass

    @abstractmethod
    def add(self, component):
        pass

    @abstractmethod
    def remove(self, component):
        pass

class Task(TaskComponent):
    def __init__(self, title, description=None, due_date=None, priority=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.is_completed = False

    def display(self, indent=0):
        print("  " * indent + f"[{'X' if self.is_completed else ' '}] {self.title}")

    def add(self, component):
        raise NotImplementedError("No se puede agregar a una tarea individual")

    def remove(self, component):
        raise NotImplementedError("No se puede remover de una tarea individual")

    def __str__(self):
        return f"Tarea: {self.title}"

if __name__ == "__main__":
    # Ejemplo de uso de la clase Task
    tarea_ejemplo = Task("Hacer informe", "Investigar y redactar", "2025-05-15", "Alta")
    print(tarea_ejemplo)