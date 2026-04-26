"""
CONTROLADOR: CambioContexto (Simulador Round Robin)

Este módulo implementa el algoritmo de planificación Round Robin
para simulación de sistemas operativos, integrando:

- Cambio de contexto entre procesos
- Manejo de cola FIFO (ready queue)
- Simulación de ejecución por quantum
- Estados de procesos (LISTO, EJECUTANDOSE, ESPERANDO I/O, TERMINADO)
- Simulación de bloqueos de I/O aleatorios
- Actualización de interfaz gráfica (Vista)
- Ejecución asíncrona usando Tkinter (after)

"""

import random as rd
from Proceso import cargar_procesos


class CambioContexto:
    """
    Clase encargada de simular el planificador Round Robin.

    Actúa como CONTROLADOR dentro del patrón MVC.

    Attributes:
        vista: Interfaz gráfica donde se muestran procesos y cola.
        root: Ventana principal de Tkinter.
        quantum: Tiempo máximo de CPU por proceso.
        cola: Lista de procesos listos para ejecución (FIFO).
        procesos: Lista global de todos los procesos del sistema.
    """

    def __init__(self, vista, root):
        """
        Inicializa el controlador y conecta la acción del botón.

        Args:
            vista (Vista): Interfaz gráfica.
            root (Tk): Ventana principal de Tkinter.
        """
        self.vista = vista
        self.root = root

        self.quantum = 5
        self.cola = []

        self.vista.btn.config(command=self.iniciar)

    def iniciar(self):
        """
        Inicializa la simulación del sistema.

        Flujo:
        - Lee cantidad de procesos desde la UI
        - Carga procesos desde el modelo
        - Inicializa la cola de ejecución
        - Renderiza la tabla en la UI
        - Inicia el ciclo del scheduler
        """
        cantidad = int(self.vista.entry.get())

        self.procesos = cargar_procesos(cantidad)
        self.cola = self.procesos.copy()

        self.vista.crear_tabla(self.procesos)
        self.vista.actualizar_cola(self.cola)
        self.ejecutar()

    def ejecutar(self):
        """
        Ejecuta un ciclo del scheduler Round Robin.

        Flujo:
        - Toma el primer proceso de la cola
        - Lo marca como EJECUTANDOSE
        - Calcula tiempo de ejecución según quantum
        - Reduce tiempo restante
        - Programa ejecución con after()
        """

        if not self.cola:
            print("TERMINADO")
            return

        proc = self.cola.pop(0)
        proc.estado = "EJECUTANDOSE"

        self.vista.actualizar(self.procesos)

        tiempo = min(proc.tiempoRestante, self.quantum)
        proc.tiempoRestante -= tiempo

        def despues():
            """
            Callback ejecutado después del quantum.

            Decide el destino del proceso:
            - Si aún tiene tiempo:
                • Puede ir a I/O (10% probabilidad)
                • O regresar a LISTO
            - Si termina:
                • Se marca como TERMINADO

            Luego actualiza UI y reinicia ciclo.
            """

            if proc.tiempoRestante > 0:

                if rd.random() < 0.1:
                    proc.estado = "ESPERANDO I/O"
                    self.cola.append(proc)

                else:
                    proc.estado = "LISTO"
                    self.cola.append(proc)

            else:
                proc.estado = "TERMINADO"

            self.vista.actualizar(self.procesos)
            self.vista.actualizar_cola(self.cola)

            self.root.after(1000, self.ejecutar)

        self.root.after(tiempo * 1000, despues)