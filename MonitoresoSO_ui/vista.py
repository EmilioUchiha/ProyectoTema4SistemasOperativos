"""
MÓDULO: Vista (MVC - Simulador de Cambio de Contexto)

DESCRIPCIÓN GENERAL:
Este módulo implementa la capa de VISTA dentro de un patrón MVC.

Su responsabilidad es exclusivamente la representación visual del sistema,
incluyendo:

- Tabla principal de procesos
- Actualización de estados de procesos
- Visualización de cola de procesos (ready queue)
- Interfaz gráfica basada en Tkinter

NO contiene lógica de negocio ni planificación de CPU.
Solo renderiza información recibida del controlador.

El diseño simula un monitor de procesos tipo sistema operativo.
"""

import tkinter as tk


class Vista:
    """
    Clase encargada de la interfaz gráfica del simulador.

    Funciona como capa de presentación en MVC.

    Attributes:
        root (Tk): Ventana principal.
        entry (Entry): Campo para ingresar cantidad de procesos.
        btn (Button): Botón de inicio de simulación.
        labels (list): Referencias a widgets de la tabla principal.
        cola_labels (list): Widgets de la cola de procesos.
    """

    def __init__(self, root):
        """
        Inicializa la interfaz gráfica principal.

        Args:
            root (Tk): Ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Simulador Cambio de contexto MVC")

        # Configuración de grid para alineación tipo tabla
        for i in range(6):
            self.root.grid_columnconfigure(i, weight=1)

        # Entrada de datos
        tk.Label(root, text="Cantidad procesos:").grid(row=0, column=0)

        self.entry = tk.Entry(root)
        self.entry.grid(row=0, column=1)

        self.btn = tk.Button(root, text="Iniciar")
        self.btn.grid(row=0, column=2)

        # Encabezados de tabla principal
        headers = ["PID", "Nombre", "CPU", "RAM", "Estado", "Tiempo"]

        for i, h in enumerate(headers):
            tk.Label(
                root,
                text=h,
                width=12,
                borderwidth=1,
                relief="solid"
            ).grid(row=1, column=i, sticky="nsew")

        self.labels = []

        # Título de cola de procesos
        tk.Label(
            self.root,
            text="COLA DE PROCESOS",
            font=("Arial", 10, "bold")
        ).grid(row=100, column=0, columnspan=6, sticky="w")

        self.cola_labels = []

    def crear_tabla(self, procesos):
        """
        Crea la tabla inicial de procesos en la interfaz.

        Args:
            procesos (list): Lista de objetos Proceso.

        Cada fila representa un proceso con sus atributos:
        PID, nombre, uso CPU, memoria, estado y tiempo restante.
        """

        self.labels.clear()

        for i, p in enumerate(procesos):

            lbl_pid = tk.Label(self.root, text=p.pid, width=12, relief="solid")
            lbl_name = tk.Label(self.root, text=p.proc, width=30, relief="solid")
            lbl_cpu = tk.Label(self.root, text=p.uso, width=12, relief="solid")
            lbl_ram = tk.Label(self.root, text=round(p.memory, 2), width=12, relief="solid")
            lbl_state = tk.Label(self.root, text=p.estado, width=30, relief="solid")
            lbl_time = tk.Label(self.root, text=p.tiempoRestante, width=12, relief="solid")

            lbl_pid.grid(row=i+2, column=0, sticky="nsew")
            lbl_name.grid(row=i+2, column=1, sticky="nsew")
            lbl_cpu.grid(row=i+2, column=2, sticky="nsew")
            lbl_ram.grid(row=i+2, column=3, sticky="nsew")
            lbl_state.grid(row=i+2, column=4, sticky="nsew")
            lbl_time.grid(row=i+2, column=5, sticky="nsew")

            # Guardamos referencias para actualización dinámica
            self.labels.append((lbl_cpu, lbl_ram, lbl_state, lbl_time))

    def actualizar(self, procesos):
        """
        Actualiza la tabla principal de procesos.

        Args:
            procesos (list): Lista de procesos actualizados.

        Se actualizan:
        - Uso de CPU
        - Memoria
        - Estado del proceso
        - Tiempo restante

        También se aplican colores según el estado.
        """

        for i, p in enumerate(procesos):

            cpu, ram, state, tiempo = self.labels[i]

            cpu.config(text=p.uso)
            ram.config(text=round(p.memory, 2))
            state.config(text=p.estado)
            tiempo.config(text=p.tiempoRestante)

            # Colores por estado (simulación visual del SO)
            if p.estado == "LISTO":
                state.config(bg="yellow", fg="black")
            elif p.estado == "EJECUTANDOSE":
                state.config(bg="red", fg="white")
            elif p.estado == "ESPERANDO I/O":
                state.config(bg="orange")
            elif p.estado == "TERMINADO":
                state.config(bg="green", fg="white")
            elif p.estado == "GUARDANDO ESTADO":
                state.config(bg="orange", fg="black")

    def actualizar_cola(self, cola):
        """
        Actualiza la representación visual de la cola de procesos.

        Args:
            cola (list): Procesos en estado listo o en cola FIFO.

        La cola se muestra como una tabla simplificada con:
        - PID
        - Nombre del proceso

        Representa el estado del scheduler en tiempo real.
        """

        # Limpia visualización anterior
        for lbl in self.cola_labels:
            lbl.destroy()

        self.cola_labels.clear()

        # Encabezados de la cola
        tk.Label(
            self.root,
            text="PID",
            width=10,
            relief="solid",
            bg="gray"
        ).grid(row=101, column=0, sticky="nsew")

        tk.Label(
            self.root,
            text="Nombre",
            width=25,
            relief="solid",
            bg="gray"
        ).grid(row=101, column=1, sticky="nsew")

        # Render de cola
        for i, p in enumerate(cola):

            lbl_pid = tk.Label(
                self.root,
                text=f"P{p.pid}",
                relief="solid",
                borderwidth=1,
                bg="lightblue"
            )

            lbl_name = tk.Label(
                self.root,
                text=p.proc,
                relief="solid",
                borderwidth=1,
                bg="lightgray"
            )

            lbl_pid.grid(row=102 + i, column=0, sticky="nsew")
            lbl_name.grid(row=102 + i, column=1, sticky="nsew")

            self.cola_labels.append(lbl_pid)
            self.cola_labels.append(lbl_name)