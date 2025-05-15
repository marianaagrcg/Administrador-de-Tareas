from core.task import Task

class TaskBuilder:
    def __init__(self, title):
        self.title = title
        self.description = None
        self.due_date = None
        self.priority = None

    def set_description(self, description):
        self.description = description
        return self

    def set_due_date(self, due_date):
        self.due_date = due_date
        return self

    def set_priority(self, priority):
        self.priority = priority
        return self

    def build(self):
        return Task(self.title, self.description, self.due_date, self.priority)

if __name__ == "__main__":
    # Ejemplo de uso del Builder
    task1 = TaskBuilder("Comprar pan").set_priority("Media").build()
    task2 = TaskBuilder("Llamar al doctor").set_due_date("Martes").set_description("Pedir cita").build()
    print(task1)
    print(task2)