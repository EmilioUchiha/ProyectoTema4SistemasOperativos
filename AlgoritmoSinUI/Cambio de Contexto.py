# Cambio de Contexto
import time , random


class Proceso:
    def __init__(self,id,tiempo):
        self.id = id
        self.tiempoRestante = tiempo
        self.estado = ''

def CambiodeContexto(procesos , quantum):
    print(f'Cambio de Proceso\n')
    colaprocesos = procesos.copy()
    while colaprocesos:
        proceso = colaprocesos.pop(0)
        proceso.estado = 'EN PROCESO'
        print(f'El proceso: {proceso.id} en proceso')
        tiempo = min(proceso.tiempoRestante,quantum)
        time.sleep(tiempo)
        proceso.tiempoRestante -= tiempo

        if proceso.tiempoRestante>0:
            proceso.estado = 'PROCESANDO'
            colaprocesos.append(proceso)
            print(f'El proceso{proceso.id} se encuentra {proceso.estado} , tiempo restante: {proceso.tiempoRestante} [s]')
        else:
            proceso.estado = 'Terminado'
            print(f'El proceso {proceso.id} se encuentra {proceso.estado}')

        print("\n")

    print(f'Todos los procesos han terminado')


def main():
    listaProcesos = [
        Proceso(1, random.randint(5,15)), # Se crea el proceso y se le da un tiempo entre 5 y 15
        Proceso(2, random.randint(5,15)),
        Proceso(3, random.randint(5,15)),
        Proceso(4, random.randint(5,15)),
    ]
    Quantum = 5 #El quantum se ajusta segun el contexto

    CambiodeContexto(listaProcesos,Quantum)

if __name__ == '__main__':
    main()