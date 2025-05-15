from core.composite import TaskList

class TaskManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskManager, cls).__new__(cls)
            cls._instance.task_lists = []  # Cambiamos task_list a task_lists para almacenar múltiples listas
        return cls._instance

    def add_list(self, task_list):
        self.task_lists.append(task_list)

    def get_all_lists(self):
        return self.task_lists

    def create_new_list(self, name):
        new_list = TaskList(name)
        self.add_list(new_list)
        return new_list

    def get_list_by_name(self, name):
        for task_list in self.task_lists:
            if task_list.name == name:
                return task_list
        return None

if __name__ == "__main__":
    # Example usage
    manager1 = TaskManager()
    list1 = manager1.create_new_list("Trabajo")
    manager1.create_new_list("Hogar")

    manager2 = TaskManager()

    print("Listas en manager1:", [tl.name for tl in manager1.get_all_lists()])
    print("Listas en manager2:", [tl.name for tl in manager2.get_all_lists()])
    print("¿Son la misma instancia?", manager1 is manager2)

    trabajo_list = manager1.get_list_by_name("Trabajo")
    if trabajo_list:
        print(f"Lista 'Trabajo' encontrada: {trabajo_list.name}")
    else:
        print("Lista 'Trabajo' no encontrada.")