from core.builder import TaskBuilder
from core.task import Task
from core.composite import TaskList
from core.command import AddTaskCommand, CompleteTaskCommand, CommandInvoker
from core.task_manager import TaskManager  # Importa TaskManager

def mostrar_menu():
    print("\n--- Administrador de Tareas ---")
    print("1. Agregar tarea a una lista")
    print("2. Crear nueva lista de tareas")
    print("3. Mostrar tareas de una lista")
    print("4. Marcar tarea como completada")
    print("5. Deshacer última acción")
    print("6. Salir")

def obtener_lista_existente():
    task_manager = TaskManager()
    listas = task_manager.get_all_lists()
    if not listas:
        print("No hay listas de tareas creadas.")
        return None
    print("Listas de tareas disponibles:")
    for i, lista in enumerate(listas):
        print(f"{i + 1}. {lista.name}")
    try:
        seleccion = int(input("Seleccione el número de la lista: ")) - 1
        if 0 <= seleccion < len(listas):
            return listas[seleccion]
        else:
            print("Selección inválida.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None

def obtener_tarea_individual(task_list):
    if not isinstance(task_list, TaskList) or not task_list.components:
        print("No hay tareas en esta lista.")
        return None
    print("Tareas disponibles:")
    tarea_counter = 1
    tareas_encontradas = []

    def _recorrer_componentes(componente):
        nonlocal tarea_counter, tareas_encontradas
        if isinstance(componente, Task):
            print(f"{tarea_counter}. {componente}")
            tareas_encontradas.append(componente)
            tarea_counter += 1
        elif isinstance(componente, TaskList):
            for sub_componente in componente.components:
                _recorrer_componentes(sub_componente)

    _recorrer_componentes(task_list)

    if not tareas_encontradas:
        print("No se encontraron tareas individuales para marcar como completadas.")
        return None

    try:
        seleccion = int(input("Seleccione el número de la tarea: ")) - 1
        if 0 <= seleccion < len(tareas_encontradas):
            return tareas_encontradas[seleccion]
        else:
            print("Selección inválida.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None

def agregar_tarea(task_list, invoker):
    titulo = input("Ingrese el título de la tarea: ")
    descripcion = input("Ingrese la descripción (opcional): ")
    prioridad = input("Ingrese la prioridad (opcional): ")
    tarea = TaskBuilder(titulo).set_description(descripcion).set_priority(prioridad).build()
    comando = AddTaskCommand(task_list, tarea)
    invoker.execute_command(comando)
    print(f"Tarea '{titulo}' agregada a la lista '{task_list.name}'.")

def crear_nueva_lista_tareas():
    task_manager = TaskManager()
    nombre_lista = input("Ingrese el nombre de la nueva lista de tareas: ")
    nueva_lista = task_manager.create_new_list(nombre_lista)
    print(f"Lista de tareas '{nombre_lista}' creada.")

def mostrar_tareas(task_list):
    task_list.display()

def marcar_completada(invoker):
    lista_seleccionada = obtener_lista_existente()
    if lista_seleccionada:
        tarea_a_completar = obtener_tarea_individual(lista_seleccionada)
        if tarea_a_completar:
            comando = CompleteTaskCommand(tarea_a_completar)
            invoker.execute_command(comando)
            print(f"Tarea '{tarea_a_completar.title}' marcada como completada en la lista '{lista_seleccionada.name}'.")

if __name__ == "__main__":
    invocador = CommandInvoker()
    task_manager = TaskManager() # Obtener la instancia del TaskManager

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            lista_seleccionada = obtener_lista_existente()
            if lista_seleccionada:
                agregar_tarea(lista_seleccionada, invocador)
        elif opcion == '2':
            crear_nueva_lista_tareas()
        elif opcion == '3':
            lista_seleccionada = obtener_lista_existente()
            if lista_seleccionada:
                mostrar_tareas(lista_seleccionada)
        elif opcion == '4':
            marcar_completada(invocador)
        elif opcion == '5':
            invocador.undo_last_command()
            print("Última acción deshecha.")
        elif opcion == '6':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")