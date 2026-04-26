import psutil as ps
import time
import random as rd

class Proceso:
    def __init__(self, pid, proceso,uso,memoria,tiempo):
        self.pid = pid
        self.proc = proceso
        self.usage = uso
        self.memory = memoria
        self.tiempoRestante = tiempo
        self.estado = 'LISTO'

def obtener_informacion_sistema():
    print("Información del Sistema:")
    print(f"CPU: {ps.cpu_percent()}%")
    print(f"Memoria: {ps.virtual_memory().percent}%")
    print(f"Disco: {ps.disk_usage('/').percent}%")
        
def carga_procesos(cantidad):
    procesos = []
    for proc in ps.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        procesos.append(Proceso(proc.info['pid'], proc.info['name'], proc.info['cpu_percent'], proc.info['memory_percent'], rd.randint(15, 25)))
        if len(procesos) >= cantidad:
            break
    return procesos

def obtener_informacion_procesos(procesos , completo , PID):
    if completo:
        print("Información de Procesos:")
        for proc in procesos:
            print(f"PID: {proc.pid} | Nombre: {proc.proc} | Uso: {proc.usage}% | Memoria: {round(proc.memory, 2)}% | Estado: {proc.estado} | Tiempo Restante: {proc.tiempoRestante} [s]")
    else:
        for proc in procesos:
            if proc.pid == PID:
                print(f"PID: {proc.pid} | Nombre: {proc.proc} | Uso: {proc.usage}% | Memoria: {round(proc.memory, 2)}% | Estado: {proc.estado} | Tiempo Restante: {proc.tiempoRestante} [s]")
                break
        else:
            print("Proceso no encontrado.")
def cambio_de_contexto(procesos, quantum):
    print(f'Cambio de Proceso\n')
    colaprocesos = procesos.copy()
    while colaprocesos:
        proc = colaprocesos.pop(0)
        proc.estado = 'EJECUTANDOSE'
        obtener_informacion_procesos(procesos, completo=False, PID=proc.pid)
        
    
    

def main():
    print("Monitoreo del Sistema Operativo\n")
    obtener_informacion_sistema()
    print("\n")
    cantidad_procesos = int(input("Ingrese la cantidad de procesos a mostrar: "))
    procesos = carga_procesos(cantidad_procesos)
    quantum = int(input("Ingrese el quantum para el cambio de contexto (en segundos): "))
    obtener_informacion_procesos(procesos, completo=True, PID=None)
    print("\n")
    cambio_de_contexto(procesos,quantum)
if __name__ == "__main__":
    main()
    