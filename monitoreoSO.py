import psutil as ps
import time

class Proceso:
    def __init__(self, pid, proceso,uso,memoria):
        self.pid = pid
        self.proc = proceso
        self.usage = uso
        self.memory = memoria
        self.estado = 'Ejecutandose'

def obtener_informacion_sistema():
    print("Información del Sistema:")
    print(f"CPU: {ps.cpu_percent()}%")
    print(f"Memoria: {ps.virtual_memory().percent}%")
    print(f"Disco: {ps.disk_usage('/').percent}%")
        
def carga_procesos():
    procesos = []
    for proc in ps.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        procesos.append(Proceso(proc.info['pid'], proc.info['name'], proc.info['cpu_percent'], proc.info['memory_percent']))
    return procesos

def obtener_informacion_procesos():
    print("Información de Procesos:")
    procesos = carga_procesos()
    for proc in procesos:
        print(f"PID: {proc.pid} | Nombre: {proc.proc} | Uso: {proc.usage}% | Memoria: {round(proc.memory, 2)}% | Estado: {proc.estado} ")

def cambio_de_contexto():
    pass

def main():
    print("Monitoreo del Sistema Operativo\n")
    obtener_informacion_sistema()
    print("\n")
    obtener_informacion_procesos()

if __name__ == "__main__":
    main()
    