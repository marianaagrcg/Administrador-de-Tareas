import streamlit as st
from core.builder import TaskBuilder
from core.task import Task
from core.composite import TaskList
from core.command import AddTaskCommand, CompleteTaskCommand, CommandInvoker
from core.task_manager import TaskManager

# Inicializar TaskManager e Invocador
task_manager = TaskManager()
invoker = CommandInvoker()

# Función para agregar una nueva tarea a una lista
def agregar_nueva_tarea(lista_tareas):
    with st.form(key=f"agregar_tarea_{lista_tareas.name}"):
        st.subheader(f"Agregar nueva tarea a '{lista_tareas.name}'")
        titulo = st.text_input("Título:")
        descripcion = st.text_area("Descripción (opcional):")
        prioridad = st.selectbox("Prioridad (opcional):", [None, "Baja", "Media", "Alta"])
        submitted = st.form_submit_button("Agregar Tarea")

        if submitted and titulo:
            tarea = TaskBuilder(titulo).set_description(descripcion).set_priority(prioridad).build()
            comando = AddTaskCommand(lista_tareas, tarea)
            invoker.execute_command(comando)
            st.success(f"Tarea '{titulo}' agregada a '{lista_tareas.name}'")

# Función para marcar una tarea como completada
def marcar_tarea_completada(lista_tareas):
    tarea_a_completar = st.selectbox(
        f"Seleccionar tarea para completar en '{lista_tareas.name}':",
        [f"{i+1}. {tarea.title}" for i, tarea in enumerate(obtener_tareas_individuales(lista_tareas))]
    )
    if tarea_a_completar:
        if st.button(f"Completar '{tarea_a_completar.split('. ')[1]}'"):
            tarea_encontrada = next((tarea for tarea in obtener_tareas_individuales(lista_tareas) if tarea.title == tarea_a_completar.split('. ')[1]), None)
            if tarea_encontrada:
                comando = CompleteTaskCommand(tarea_encontrada)
                invoker.execute_command(comando)
                st.success(f"Tarea '{tarea_encontrada.title}' marcada como completada.")

# Función para obtener todas las tareas individuales de una lista (recursivamente)
def obtener_tareas_individuales(componente):
    tareas = []
    if isinstance(componente, Task):
        tareas.append(componente)
    elif isinstance(componente, TaskList):
        for sub_componente in componente.components:
            tareas.extend(obtener_tareas_individuales(sub_componente))
    return tareas

# Interfaz principal de Streamlit
st.title("Administrador de Tareas con Patrones de Diseño")

# Sidebar para la gestión de listas
with st.sidebar:
    st.subheader("Gestión de Listas")
    nueva_lista_nombre = st.text_input("Nombre de la nueva lista:")
    if st.button("Crear Nueva Lista"):
        if nueva_lista_nombre:
            task_manager.create_new_list(nueva_lista_nombre)
            st.success(f"Lista '{nueva_lista_nombre}' creada.")

    lista_seleccionada_nombre = st.selectbox("Seleccionar lista de tareas:", [lista.name for lista in task_manager.get_all_lists()])
    lista_seleccionada = task_manager.get_list_by_name(lista_seleccionada_nombre) if lista_seleccionada_nombre else None

# Mostrar tareas de la lista seleccionada
if lista_seleccionada:
    st.subheader(f"Tareas en '{lista_seleccionada.name}'")
    for componente in lista_seleccionada.components:
        if isinstance(componente, Task):
            st.checkbox(componente.title, value=componente.is_completed, disabled=True)
        elif isinstance(componente, TaskList):
            st.write(f"**{componente.name}**")
            for sub_componente in componente.components:
                if isinstance(sub_componente, Task):
                    st.markdown(f"- [ ] {sub_componente.title}") # Simple representación para sub-tareas

    st.markdown("---")

    # Sección para agregar nuevas tareas y marcar como completadas
    col1, col2 = st.columns(2)
    with col1:
        agregar_nueva_tarea(lista_seleccionada)
    with col2:
        marcar_tarea_completada(lista_seleccionada)

    # Botón para deshacer la última acción
    if st.button("Deshacer Última Acción"):
        invoker.undo_last_command()
        st.info("Última acción deshecha.")

else:
    st.info("Crea o selecciona una lista de tareas en la barra lateral.")