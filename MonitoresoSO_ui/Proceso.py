"""
MÓDULO: Modelo de Procesos (Simulación de Sistema Operativo)

Este módulo define la estructura base de un proceso y la función encargada
de simular la obtención de procesos activos del sistema operativo utilizando psutil.

Se utiliza como capa de MODELO dentro de un patrón MVC.
"""
import psutil as ps
import random as rd


class Proceso:
    """
    Representa un proceso del sistema dentro de la simulación.

    Attributes:
        pid (int): Identificador del proceso en el sistema operativo.
        proc (str): Nombre del proceso.
        uso (float): Porcentaje de uso de CPU.
        memory (float): Porcentaje de uso de memoria RAM.
        tiempoRestante (int): Tiempo simulado de ejecución restante.
        estado (str): Estado actual del proceso en la simulación.
    """

    def __init__(self, pid, proceso, uso, memoria, tiempo):
        self.pid = pid
        self.proc = proceso
        self.uso = uso
        self.memory = memoria
        self.tiempoRestante = tiempo
        self.estado = "LISTO"


def cargar_procesos(cantidad):
    """
    Carga procesos reales del sistema operativo usando psutil
    y los convierte en objetos de simulación.

    IMPORTANTE:
    - psutil.process_iter() recorre procesos reales del sistema.
    - Devuelve objetos tipo Process (no listas simples).
    - Se debe acceder a sus atributos con proc.info.

    Args:
        cantidad (int): Número máximo de procesos a cargar.

    Returns:
        list[Proceso]: Lista de procesos simulados basados en procesos reales.

    Flujo:
        1. Itera procesos reales del sistema operativo.
        2. Extrae PID, nombre, CPU y memoria.
        3. Genera tiempo aleatorio de ejecución.
        4. Crea objetos Proceso.
        5. Limita la cantidad según parámetro.
    """

    procesos = []

    # Iterador seguro de procesos del sistema
    for proc in ps.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procesos.append(
                Proceso(
                    proc.info['pid'],
                    proc.info['name'],
                    proc.info['cpu_percent'],
                    proc.info['memory_percent'],
                    rd.randint(6, 15)
                )
            )

            if len(procesos) >= cantidad:
                break

        except (ps.NoSuchProcess, ps.AccessDenied):
            # Algunos procesos del sistema pueden desaparecer o bloquear acceso
            continue

    return procesos