import tkinter as tk
import random


class Proceso:
    """Representa un proceso dentro de la simulación de un sistema operativo.

    Atributos:
        id (int): Identificador del proceso (PID).
        tiempo_restante (int): Tiempo de CPU que aún necesita el proceso.
        estado (str): Estado actual del proceso (READY, RUNNING, TERMINATED).
    """

    def __init__(self, pid, tiempo):
        self.id = pid
        self.tiempo_restante = tiempo
        self.estado = "READY"


class App:
    """Simulador gráfico de planificación de CPU usando Round Robin.

    Este programa simula cómo un sistema operativo asigna tiempo de CPU
    a múltiples procesos utilizando una política de planificación Round Robin.

    Componentes principales:
        - CPU label: muestra el proceso actualmente ejecutándose.
        - Tabla: muestra los procesos, su tiempo restante y estado.
        - Log: registra eventos como cambios de contexto y finalización.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Round Robin Simulator")

        self.quantum = 3
        self.after_id = None

        self.cpu_label = tk.Label(root, text="CPU: IDLE", font=("Arial", 14), bg="black", fg="white")
        self.cpu_label.grid(row=0, column=0, columnspan=3, sticky="we", pady=5)

        self.boton = tk.Button(root, text="Iniciar", command=self.iniciar)
        self.boton.grid(row=1, column=0, columnspan=3, pady=5)

        self.tabla = tk.Frame(root)
        self.tabla.grid(row=2, column=0)

        tk.Label(self.tabla, text="Proceso", width=10, relief="solid").grid(row=0, column=0)
        tk.Label(self.tabla, text="Tiempo", width=10, relief="solid").grid(row=0, column=1)
        tk.Label(self.tabla, text="Estado", width=12, relief="solid").grid(row=0, column=2)

        self.labels = []

        self.log = tk.Text(root, height=12, width=40)
        self.log.grid(row=2, column=1, columnspan=2, padx=10)

    def escribir_log(self, msg):
        """Agrega un mensaje al registro de eventos del sistema."""
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def iniciar(self):
        """Inicializa la simulación:
        - Cancela ejecuciones anteriores.
        - Limpia la interfaz.
        - Genera nuevos procesos.
        - Inicia el scheduler Round Robin.
        """

        if self.after_id:
            self.root.after_cancel(self.after_id)

        self.log.delete("1.0", tk.END)

        self.procesos = [
            Proceso(1, random.randint(5, 15)),
            Proceso(2, random.randint(5, 15)),
            Proceso(3, random.randint(5, 15)),
            Proceso(4, random.randint(5, 15)),
        ]

        self.cola = self.procesos.copy()

        for w in self.tabla.winfo_children():
            if int(w.grid_info()["row"]) > 0:
                w.destroy()

        self.labels.clear()

        for i, p in enumerate(self.procesos):
            lbl1 = tk.Label(self.tabla, text=f"P{p.id}", width=10, relief="solid")
            lbl2 = tk.Label(self.tabla, text=p.tiempo_restante, width=10, relief="solid")
            lbl3 = tk.Label(self.tabla, text=p.estado, width=12, relief="solid")

            lbl1.grid(row=i + 1, column=0)
            lbl2.grid(row=i + 1, column=1)
            lbl3.grid(row=i + 1, column=2)

            self.labels.append((lbl2, lbl3))

        self.ejecutar()

    def actualizar(self):
        """Actualiza la interfaz gráfica con el estado actual de los procesos."""
        for i, p in enumerate(self.procesos):
            t, e = self.labels[i]
            t.config(text=p.tiempo_restante)

            color = {
                "READY": "lightgray",
                "RUNNING": "orange",
                "TERMINATED": "lightgreen"
            }[p.estado]

            e.config(text=p.estado, bg=color)

    def ejecutar(self):
        """Ejecuta la lógica del scheduler Round Robin.

        Selecciona procesos de la cola, simula ejecución en CPU
        y maneja el cambio de contexto.
        """

        if not self.cola:
            self.cpu_label.config(text="CPU: IDLE")
            self.escribir_log(" Todos los procesos terminados")
            return

        proceso = self.cola.pop(0)

        self.escribir_log(f" Context Switch → P{proceso.id}")

        proceso.estado = "RUNNING"
        self.cpu_label.config(text=f"CPU: P{proceso.id}")

        self.actualizar()

        tiempo = min(proceso.tiempo_restante, self.quantum)

        self.after_id = self.root.after(
            tiempo * 500,
            lambda: self.finalizar(proceso, tiempo)
        )

    def finalizar(self, proceso, tiempo):
        """Finaliza o replanifica un proceso después de su quantum."""

        proceso.tiempo_restante -= tiempo

        if proceso.tiempo_restante <= 0:
            proceso.estado = "TERMINATED"
            self.escribir_log(f" P{proceso.id} terminado")
        else:
            proceso.estado = "READY"
            self.cola.append(proceso)

        self.actualizar()
        self.ejecutar()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()